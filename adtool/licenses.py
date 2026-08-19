from adtool.graph_client import get_client
from adtool import dryrun

def list_skus(print_sku=False) -> dict:
    http_client = get_client()
    response = http_client.get("/subscribedSkus")
    response.raise_for_status()

    parsed_response = response.json()
    skus = parsed_response.get("value", [])

    index = 0
    for sku in skus:
        index += 1
        # each sku is a dict
        part_number = sku["skuPartNumber"]
        enabled = sku["prepaidUnits"]["enabled"]
        consumed = sku["consumedUnits"]
        if print_sku is True:
            print(f"{index}) {part_number}: {consumed}/{enabled} seats used")

    return skus

def get_user_licenses(user_id: str) -> list[dict]:
    client = get_client()
    response = client.get(f"/users/{user_id}?$select=assignedLicenses")
    response.raise_for_status()
    return response.json().get("assignedLicenses", [])

def assign_license(user_id: str, skus_to_assign: dict) -> dict:
    url = f"/users/{user_id}/assignLicense"

    sku_assign_list = []
    sku_remove_list = []
    for sku in skus_to_assign:
        sku_id = sku["skuId"]
        if sku["should_assign_sku"] == True:
            sku_assign_list.insert(0, {"skuId": sku_id})
        elif sku["should_assign_sku"] == False:
            sku_remove_list.insert(0, {"skuId": sku_id})


    payload = {
        "addLicenses": sku_assign_list,
        "removeLicenses": sku_remove_list
    }
    
    if dryrun.is_dry_run():
        dryrun.log_would_send("POST", url , payload)
        return None

    http_client = get_client()
    response = http_client.post(url, json=payload)
    if response.status_code >= 400:
        print(f"=== Graph error body ===\n{response.text}\n============================")
    response.raise_for_status()
    return response.json()

list_skus()
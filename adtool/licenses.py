from adtool.graph_client import get_client
from adtool import dryrun

def list_skus():
    http_client = get_client()
    response = http_client.get("/subscribedSkus")
    response.raise_for_status()

    parsed_response = response.json()
    skus = parsed_response.get("value", {})

    index = 0
    for sku in skus:
        index += 1
        # each sku is a dict
        part_number = sku["skuPartNumber"]
        enabled = sku["prepaidUnits"]["enabled"]
        consumed = sku["consumedUnits"]
        print(f"{index}) {part_number}: {consumed}/{enabled} seats used")

    #print(body.get("addLicenses", {}))
    #print(body.get("removeLicenses", {}))

def assign_license(userid):
    http_client = get_client()

    if dryrun.is_dry_run():
        dryrun.log_would_send(f"/users"userid"/assignLicense")
        
    response = http_client.post()


list_skus()
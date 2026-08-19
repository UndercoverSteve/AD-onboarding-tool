from adtool import config
from adtool import graph_client
from adtool import dryrun
from adtool import licenses
from adtool import prompts

import secrets
import string

def get_people():
    client = graph_client.get_client()
    response = client.get("/users?$top=10")
    response.raise_for_status()
    
    parsed_response = response.json()

    users = parsed_response["value"]

    names = []

    for user in users:
        displayName = user["displayName"]
        names.append(displayName)

    return users

def generate_password(length: int = 16) -> str:
    alphabet = string.ascii_letters + string.digits + "!@#$%^&*"
    while True:
        pw = "".join(secrets.choice(alphabet) for _ in range(length))
        if (any(c.islower() for c in pw)
            and any(c.isupper() for c in pw)
            and any(c.isdigit() for c in pw)
            and any(c in "!@#$%^&*" for c in pw)):
            return pw

def create_user(user_info: dict) -> dict:
    first_name = user_info["first_name"]
    last_name = user_info["last_name"]
    manager_upn = user_info["manager_upn"]

    display_name = f"{first_name} {last_name}"
    mail_nickname = first_name[0].lower() + last_name.lower()
    user_principal_name = mail_nickname + "@" + config.TENANT_DOMAIN

    password = generate_password()
    print(f"Temporary password (share with user): {password}")
    
    payload = {
        "accountEnabled": True,
        "displayName": display_name,
        "givenName": first_name,
        "surname": last_name,
        "mailNickname": mail_nickname,
        "userPrincipalName": user_principal_name,
        "department": user_info["department"],
        "jobTitle": user_info["job_title"],
        "passwordProfile": {
            "forceChangePasswordNextSignIn": True,
            "password": password
        },
    }

    # Do a trial run, do not actually post
    if dryrun.is_dry_run():
        dryrun.log_would_send("POST", "/users", payload)
        return None

    http_client = graph_client.get_client()

    response = http_client.post("/users", json=payload)
    response.raise_for_status()
    return response.json()

def onboard_user_flow():
    user_dict = prompts.prompt_new_user()
    if user_dict is None:
        return
    
    new_user = create_user(user_dict)

    # If dry running, continue
    if new_user is None:
        print("Dry running onboard_user_flow, continuing")
        user_id = 0
    else:
        user_id = new_user["id"]

    # Prompt user for what SKUs they want to assign. This will return a dictionary for what to assign and remove.
    skus_to_assign = prompts.prompt_sku_choice(user_id)
    licenses.assign_license(user_id, skus_to_assign)

# Manage users (assign licenses)
def people_manager():
    people_dict = get_people()
    index = 0
    for p in people_dict:
        index += 1
        print(f"{index}) {p["displayName"]}")

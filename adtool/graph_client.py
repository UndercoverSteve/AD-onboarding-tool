from adtool import config
import msal
import httpx

app = msal.ConfidentialClientApplication(client_id=config.CLIENT_ID, client_credential=config.CLIENT_SECRET, authority=f"https://login.microsoftonline.com/{config.TENANT_ID}")

def get_token():
    token_query = app.acquire_token_for_client(scopes=["https://graph.microsoft.com/.default"])
    if "error" in token_query:
        raise ValueError("ERROR! Retrieving access token failed! Error: " + token_query["error"] + " Description: " + token_query["error_description"])
    return token_query["access_token"]

def get_client():
    token = get_token()
    http_client = httpx.Client(
        base_url="https://graph.microsoft.com/v1.0",
        headers={"Authorization": f"Bearer {token}"}
    )
    return http_client
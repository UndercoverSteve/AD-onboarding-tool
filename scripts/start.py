from adtool.graph_client import get_client

def get_people():
    client = get_client()
    response = client.get("/users?$top=10")
    response.raise_for_status()
    
    parsed_response = response.json()

    users = parsed_response["value"]

    names = []

    for user in users:
        displayName = user["displayName"]
        names.append(displayName)

    print(names)

get_people()

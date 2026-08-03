import os
from dotenv import load_dotenv

load_dotenv()

TENANT_ID = os.getenv("TENANT_ID")
CLIENT_ID = os.getenv("CLIENT_ID")
CLIENT_SECRET = os.getenv("CLIENT_SECRET")

DRY_RUN = os.getenv("DRY_RUN", "true").lower() == "true"

configs = {"TENANT_ID":TENANT_ID, "CLIENT_ID":CLIENT_ID, "CLIENT_SECRET":CLIENT_SECRET}

# Check defs to see if a value is missing, warn user if so
def check_defs():
    missing = []
    for name, config in configs.items():
        if config is None:
            missing.append(name)
    if missing:
        raise ValueError("There are defs missing! Missing defs: " + " ".join(missing))

check_defs()
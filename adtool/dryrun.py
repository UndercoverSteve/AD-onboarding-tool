from adtool import config
import json

def is_dry_run() -> bool:
    return config.DRY_RUN

def log_would_send(method: str, url: str, payload: dict) -> None:
    print("[DRY RUN] Would " + method + " " + url)
    log = json.dumps(payload, indent=2)
    print(log)


import json
import yaml
import os


DEFAULT_MAIN_PROGRESS = {
    "captured": {
        "count": 0,
        "list": {
            "<kingdom name>": {
                "count": 0,
                "full": False,
                "list": []
            }
        }
    },
    "terminals": {
        "count": 0,
        "list": []
    }
}

DEFAULT_KD_PROGRESS = {
    "captured": {
        "count": 0,
        "full": False,
        "list": []
    }
}

def read_main_progress():
    """
    Read the main progress.
    """
    if not os.path.exists("game/progress.json"):
        with open("game/progress.json", "w") as f:
            json.dump(DEFAULT_MAIN_PROGRESS, f, indent=4)

    with open("game/progress.json", "r") as f:
        progress = json.load(f)

    return progress


def read_kingdom_progress(kingdom_name):
    """
    Read the progress of a kingdom.
    """
    if not os.path.exists(f"game/maps/{kingdom_name}/progress.json"):
        with open(f"game/maps/{kingdom_name}/progress.json", "w") as f:
            json.dump(DEFAULT_KD_PROGRESS, f, indent=4)

    with open(f"game/maps/{kingdom_name}/progress.json", "r") as f:
        progress = json.load(f)

    return progress


def write_main_progress(progress):
    """
    Write the main progress.
    """
    with open("game/progress.json", "w") as f:
        json.dump(progress, f, indent=4)


def write_kingdom_progress(kingdom_name, progress):
    """
    Write the progress of a kingdom.
    """
    progress["captured"]["list"].remove("__START__")
    progress["captured"]["count"] = len(progress["captured"]["list"])

    with open(f"game/maps/{kingdom_name}/about.yaml", "r") as f:
        about = yaml.safe_load(f)
        if progress["captured"]["count"] == len(about["city"]["list"]):
            progress["captured"]["full"] = True

    with open(f"game/maps/{kingdom_name}/progress.json", "w") as f:
        json.dump(progress, f, indent=4)

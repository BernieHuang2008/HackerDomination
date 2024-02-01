import json


def read_main_progress():
    """
    Read the main progress.
    """
    with open("game/progress.json", "r") as f:
        progress = json.load(f)

    return progress


def read_kingdom_progress(kingdom_name):
    """
    Read the progress of a kingdom.
    """
    with open(f"game/maps/{kingdom_name}/progress.json", "r") as f:
        progress = json.load(f)

    return progress


def read_city_progress(kingdom_name, city_name):
    """
    Read the progress of a city.
    """
    with open(f"game/maps/{kingdom_name}/cities/{city_name}/progress.json", "r") as f:
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
    with open(f"game/maps/{kingdom_name}/progress.json", "w") as f:
        json.dump(progress, f, indent=4)


def write_city_progress(kingdom_name, city_name, progress):
    """
    Write the progress of a city.
    """
    with open(f"game/maps/{kingdom_name}/cities/{city_name}/progress.json", "w") as f:
        json.dump(progress, f, indent=4)

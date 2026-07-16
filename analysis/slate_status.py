import csv
import os

from utils.prop_identity import build_prop_key


PROPS_FILE = "props.csv"
PAPER_BETS_FILE = "paper_bets.csv"


def load_csv_rows(file_path):
    """
    Load rows from a CSV file.

    Returns an empty list when the file does not exist.
    """

    if not os.path.exists(file_path):
        return []

    with open(file_path, "r", newline="", encoding="utf-8") as file:
        return list(csv.DictReader(file))

def get_current_slate_status(
    props_file=PROPS_FILE,
    paper_bets_file=PAPER_BETS_FILE
):
    """
    Compare the current active slate against saved paper-bet records.

    Returns counts showing whether the current slate has been fully analyzed.
    """

    props = load_csv_rows(props_file)
    paper_bets = load_csv_rows(paper_bets_file)

    if not props:
        return {
            "game_date": None,
            "total_props": 0,
            "analyzed_props": 0,
            "remaining_props": 0,
            "complete": True,
            "status": "EMPTY"
        }

    current_game_date = props[0]["game_date"]

    current_prop_keys = {
        build_prop_key(prop)
        for prop in props
    }

    analyzed_prop_keys = {
        build_prop_key(bet)
        for bet in paper_bets
        if bet.get("game_date") == current_game_date
    }

    analyzed_count = len(
        current_prop_keys.intersection(analyzed_prop_keys)
    )

    total_count = len(current_prop_keys)
    remaining_count = total_count - analyzed_count

    if analyzed_count == 0:
        status = "NOT_ANALYZED"
    elif remaining_count == 0:
        status = "COMPLETE"
    else:
        status = "PARTIAL"

    return {
        "game_date": current_game_date,
        "total_props": total_count,
        "analyzed_props": analyzed_count,
        "remaining_props": remaining_count,
        "complete": remaining_count == 0,
        "status": status
    }
import csv
import os
import re
import shutil


RAW_PROPS_FILE = "raw_props.txt"
OUTPUT_PROPS_FILE = "props.csv"
BACKUP_FOLDER = "prop_backups"


def clean_lines(raw_text):
    """
    Clean copied PrizePicks text into usable lines.

    Lo Note:
    PrizePicks copied text has blank lines and extra UI text.
    This function removes empty lines and trims whitespace.
    """

    lines = []

    ignored_lines = {
        "Swap",
    }

    for line in raw_text.splitlines():
        line = line.strip()

        if line == "":
            continue

        if line in ignored_lines:
            continue

        lines.append(line)

    return lines


def is_team_position_line(line):
    """
    Check whether a line looks like a team/position line.

    Example:
    MIN - G
    LVA - C
    DAL - G
    """

    pattern = r"^[A-Z]{2,4}\s-\s[A-Z-]+$"

    return re.match(pattern, line) is not None

def find_prop_start_indexes(lines):
    """
    Find indexes where a new prop card likely starts.

    A prop usually starts one line before a team/position line.

    Example:
    Olivia Miles
    MIN - G
    """

    start_indexes = []

    for index, line in enumerate(lines):

        if is_team_position_line(line):
            start_index = index - 1

            if start_index >= 0:
                start_indexes.append(start_index)

    return start_indexes

def split_into_prop_blocks(lines, start_indexes):
    """
    Split cleaned lines into individual prop blocks.

    Each block should represent one copied PrizePicks card.
    """

    prop_blocks = []

    for position, start_index in enumerate(start_indexes):

        if position + 1 < len(start_indexes):
            end_index = start_indexes[position + 1]
        else:
            end_index = len(lines)

        block = lines[start_index:end_index]
        prop_blocks.append(block)

    return prop_blocks

def detect_risk_type(player_risk_line):
    """
    Detect whether a copied prop is NORMAL, GOBLIN, or DEMON.

    PrizePicks sometimes attaches the risk type directly to the player name.

    Example:
    A'ja WilsonGoblin
    Kelsey PlumDemon
    """

    if "Goblin" in player_risk_line:
        return "GOBLIN"

    if "Demon" in player_risk_line:
        return "DEMON"

    return "NORMAL"


def extract_opponent(matchup_line):
    """
    Extract opponent from a matchup line.

    Examples:
    vs PDX Mon 8:00pm -> PDX
    @ DAL Mon 8:00pm  -> DAL
    """

    parts = matchup_line.split()

    if len(parts) >= 2:
        return parts[1]

    return ""


def parse_prop_block(block, game_date):
    """
    Convert one copied PrizePicks prop block into a dictionary.

    Expected block pattern:
    [player/risk, team-position, clean player, matchup, line, stat, ...]
    """

    player_risk_line = block[0]
    player = block[2]
    matchup_line = block[3]
    prop_line = block[4]
    stat = block[5]

    stat_aliases = {
        "Points": "PTS",
        "Rebounds": "REB",
        "Assists": "AST",
        "PRA": "PRA",
    }

    stat = stat_aliases.get(stat, stat)

    risk_type = detect_risk_type(player_risk_line)
    opponent = extract_opponent(matchup_line)

    return {
        "sport": "WNBA",
        "player": player,
        "stat": stat,
        "line": prop_line,
        "opponent": opponent,
        "game_date": game_date,
        "risk_type": risk_type
    }

def backup_existing_props(output_file=OUTPUT_PROPS_FILE):
    """
    Back up the current props.csv before overwriting it.

    Lo Note:
    The backup filename must match the slate date stored inside
    the existing props.csv, not the date of the incoming slate.
    """

    if not os.path.exists(output_file):
        return None

    with open(output_file, "r", encoding="utf-8") as file:
        reader = csv.DictReader(file)
        first_row = next(reader, None)

    if not first_row:
        return None

    existing_game_date = first_row.get("game_date")

    if not existing_game_date:
        return None

    os.makedirs(BACKUP_FOLDER, exist_ok=True)

    backup_file = os.path.join(
        BACKUP_FOLDER,
        f"props_{existing_game_date}.csv"
    )

    shutil.copy(output_file, backup_file)

    return backup_file

def load_existing_props(output_file=OUTPUT_PROPS_FILE):
    """
    Load the current active props file.

    Returns an empty list if props.csv does not exist.
    """

    if not os.path.exists(output_file):
        return []

    with open(output_file, "r", encoding="utf-8") as file:
        reader = csv.DictReader(file)
        return list(reader)

def merge_props(existing_props, incoming_props):
    """
    Merge existing and incoming props while removing exact duplicates.

    A prop is considered a duplicate when all identifying fields match.
    """

    unique_props = {}
    key_fields = [
        "sport",
        "player",
        "stat",
        "line",
        "opponent",
        "game_date",
        "risk_type"
    ]

    for prop in existing_props + incoming_props:
        normalized_prop = prop.copy()
        normalized_prop["line"] = str(float(prop["line"]))

        prop_key = tuple(
            str(normalized_prop[field]).strip()
            for field in key_fields
        )
        unique_props[prop_key] = prop

    return list(unique_props.values())

def write_props_to_csv(props, output_file=OUTPUT_PROPS_FILE):
    """
    Write parsed props to props.csv.

    Output format matches the current active props file:
    sport,player,stat,line,opponent,game_date,risk_type
    """

    fieldnames = [
        "sport",
        "player",
        "stat",
        "line",
        "opponent",
        "game_date",
        "risk_type"
    ]

    with open(output_file, "w", newline="", encoding="utf-8") as file:
        writer = csv.DictWriter(file, fieldnames=fieldnames)

        writer.writeheader()
        writer.writerows(props)

if __name__ == "__main__":

    with open(RAW_PROPS_FILE, "r", encoding="utf-8") as file:
        raw_text = file.read()

    game_date = input("Enter slate date (YYYY-MM-DD): ")

    lines = clean_lines(raw_text)
    start_indexes = find_prop_start_indexes(lines)
    prop_blocks = split_into_prop_blocks(lines, start_indexes)
    print(f"Found {len(prop_blocks)} prop blocks")

    props = []

    for block in prop_blocks:
        prop = parse_prop_block(block, game_date)
        props.append(prop)

    parsed_count = len(props)
    props = merge_props([], props)
    incoming_duplicate_count = parsed_count - len(props)

    existing_props = load_existing_props()

    raw_existing_count = len(existing_props)
    existing_props = merge_props([], existing_props)
    existing_duplicate_count = raw_existing_count - len(existing_props)

    if existing_props:
        existing_game_date = existing_props[0].get("game_date")
    else:
        existing_game_date = None

    if existing_game_date == game_date:
        merged_props = merge_props(existing_props, props)

        existing_count = len(existing_props)
        imported_count = len(props)
        final_count = len(merged_props)
        added_count = final_count - existing_count
        duplicate_count = imported_count - added_count

        write_props_to_csv(merged_props)

        print()
        print("SAME-DATE SLATE UPDATE")
        print("-" * 50)
        print(f"Slate Date: {game_date}")
        print(f"Existing Props: {existing_count}")
        print(f"Existing Duplicates Removed: {existing_duplicate_count}")
        print(f"Imported Props: {imported_count}")
        print(f"Incoming Duplicates Removed: {incoming_duplicate_count}")
        print(f"New Props Added: {added_count}")
        print(f"Duplicates Skipped: {duplicate_count}")
        print(f"Updated Total: {final_count}")

    else:
        backup_file = backup_existing_props()

        if backup_file:
            print(f"Backed up existing props to {backup_file}")

        write_props_to_csv(props)

        print(f"Imported {len(props)} unique props into {OUTPUT_PROPS_FILE}")

        if incoming_duplicate_count:
            print(f"Removed {incoming_duplicate_count} duplicate props from raw import.")
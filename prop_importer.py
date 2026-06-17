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

    pattern = r"^[A-Z]{2,4}\s-\s[A-Z]{1,2}$"

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

def backup_existing_props(
    game_date,
    output_file=OUTPUT_PROPS_FILE
):
    """
    Back up the current props.csv before overwriting it.

    Lo Note:
    The importer overwrites props.csv, so this protects the previous
    active slate from being lost.
    """
    # Lo Note:
    # Backups are named by slate date so that historical
    # boards can be reused later for diagnostics,
    # backtesting, and engine comparisons.

    if not os.path.exists(output_file):
        return None

    os.makedirs(BACKUP_FOLDER, exist_ok=True)

    backup_file = os.path.join(
        BACKUP_FOLDER,
        f"props_{game_date}.csv"
    )

    shutil.copy(output_file, backup_file)

    return backup_file

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

    props = []

    for block in prop_blocks:
        prop = parse_prop_block(block, game_date)
        props.append(prop)

    backup_file = backup_existing_props(game_date)

    if backup_file:
        print(f"Backed up existing props to {backup_file}")

    write_props_to_csv(props)

    print(f"Imported {len(props)} props into {OUTPUT_PROPS_FILE}")
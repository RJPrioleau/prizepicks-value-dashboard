from sportsdataverse import (
    load_wnba_rosters,
    load_wnba_stats_player_game_logs
)


"""
Lo Note:

SportsDataverse roster athlete_id values do not match
SportsDataverse game log player_id values.

Current implementation uses player_name matching
for game log filtering.

Future investigation:
Determine if a reliable athlete_id -> player_id mapping exists.
"""

WNBA_SEASON = 2025
WNBA_ROSTER_CACHE = None
WNBA_GAME_LOG_CACHE = None


def get_wnba_rosters():
    """
    Load WNBA roster data from SportsDataverse.

    Lo Note:
    This is the WNBA player lookup data source.
    It gives us player names, player IDs, teams, positions, and season info.
    """

    global WNBA_ROSTER_CACHE

    if WNBA_ROSTER_CACHE is not None:
        return WNBA_ROSTER_CACHE

    rosters = load_wnba_rosters(
        seasons=[WNBA_SEASON],
        return_as_pandas=True
    )

    WNBA_ROSTER_CACHE = rosters

    return rosters

def find_wnba_player_id(player_name):
    """
    Find a WNBA player ID by full name.

    Example:
    A'ja Wilson -> 3149391
    """

    rosters = get_wnba_rosters()

    player = rosters[
        rosters["full_name"].str.lower() == player_name.lower()
    ]

    if player.empty:
        return None

    return player.iloc[0]["athlete_id"]

def get_wnba_game_logs():
    """
    Load WNBA player game logs from SportsDataverse.

    Lo Note:
    This gives us the historical box score data needed for
    last 5, last 10, season averages, hit rates, and trends.
    """

    global WNBA_GAME_LOG_CACHE

    if WNBA_GAME_LOG_CACHE is not None:
        return WNBA_GAME_LOG_CACHE

    game_logs = load_wnba_stats_player_game_logs(
        seasons=[WNBA_SEASON],
        return_as_pandas=True
    )

    WNBA_GAME_LOG_CACHE = game_logs

    return game_logs

def get_wnba_player_game_logs(player_name):
    """
    Get WNBA game logs for one player by name.

    Lo Note:
    SportsDataverse roster athlete_id does not match the game log player_id,
    so this function filters game logs by player_name for now.
    """

    game_logs = get_wnba_game_logs()

    player_logs = game_logs[
        game_logs["player_name"].str.lower() == player_name.lower()
    ]

    player_logs = add_wnba_calculated_stats(player_logs)

    return player_logs

def add_wnba_calculated_stats(df):
    """
    Add calculated stat columns needed by the analysis engine.
    """

    df = df.copy()

    df["pts"] = df["pts"].astype(float)
    df["reb"] = df["reb"].astype(float)
    df["ast"] = df["ast"].astype(float)

    df["PRA"] = df["pts"] + df["reb"] + df["ast"]

    return df

def get_wnba_player_analysis(player_name, stat_type, line):
    """
    Analyze a WNBA player's recent performance against a prop line.

    V1 Goal:
    Recreate the basic NBA-style historical analysis for WNBA using
    SportsDataverse game logs.
    """

    player_logs = get_wnba_player_game_logs(player_name)

    if player_logs.empty:
        print(f"No WNBA game logs found for {player_name}")
        return None

    if stat_type not in player_logs.columns:
        print(f"Unsupported WNBA stat type: {stat_type}")
        return None

    player_logs = player_logs.sort_values("game_date", ascending=False)

    last_5_avg = float(round(player_logs.head(5)[stat_type].mean(), 2))
    last_10_avg = float(round(player_logs.head(10)[stat_type].mean(), 2))
    season_avg = float(round(player_logs[stat_type].mean(), 2))

    hits = player_logs.head(10)[
        player_logs.head(10)[stat_type] > line
    ]

    hit_count = len(hits)
    hit_rate = round((hit_count / 10) * 100, 2)

    recent_5 = player_logs.head(5)[stat_type].mean()
    previous_5 = player_logs.iloc[5:10][stat_type].mean()
    trend_value = float(round(recent_5 - previous_5, 2))

    if trend_value > 0:
        trend_direction = "UP"
    elif trend_value < 0:
        trend_direction = "DOWN"
    else:
        trend_direction = "FLAT"

    return {
        "player": player_name,
        "stat": stat_type,
        "line": line,
        "last_5_avg": last_5_avg,
        "last_10_avg": last_10_avg,
        "season_avg": season_avg,
        "hit_count": hit_count,
        "hit_rate": hit_rate,
        "trend_direction": trend_direction,
        "trend_value": trend_value,
    }
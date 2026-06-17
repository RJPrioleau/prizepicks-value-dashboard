from sportsdataverse import (
    load_wnba_rosters,
    load_wnba_stats_player_game_logs
)
from analysis.historical_analysis import (
    calculate_recent_averages,
    calculate_hit_rate,
    calculate_trend,
    calculate_home_away_split,
    calculate_opponent_average
)
from analysis.recommendation_engine import get_basic_recommendation
from analysis.matchup_parser import parse_basketball_matchup




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

    parsed_matchups = player_logs["matchup"].apply(parse_basketball_matchup)

    player_logs["location"] = parsed_matchups.apply(lambda x: x[0])
    player_logs["opponent"] = parsed_matchups.apply(lambda x: x[1])

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

def get_wnba_player_analysis(player_name, stat_type, line, opponent=None):
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

    stat_column_map = {
        "PTS": "pts",
        "REB": "reb",
        "AST": "ast",
        "PRA": "PRA",
    }

    stat_column = stat_column_map.get(stat_type, stat_type)

    if stat_column not in player_logs.columns:
        print(f"Unsupported WNBA stat type: {stat_type}")
        return None

    player_logs = player_logs.sort_values("game_date", ascending=False)

    averages = calculate_recent_averages(player_logs, stat_column)

    last_5_avg = averages["last_5_avg"]
    last_10_avg = averages["last_10_avg"]
    season_avg = averages["season_avg"]

    hit_data = calculate_hit_rate(
        player_logs,
        stat_column,
        line
    )

    hit_count = hit_data["hit_count"]
    hit_rate = hit_data["hit_rate"]

    trend_data = calculate_trend(player_logs, stat_column)

    trend_direction = trend_data["trend_direction"]
    trend_value = trend_data["trend_value"]

    home_away_data = calculate_home_away_split(
        player_logs,
        stat_column,
        location_column="location"
    )

    home_avg = home_away_data["home_avg"]
    away_avg = home_away_data["away_avg"]

    opponent_avg = "N/A"

    if opponent is not None:
        opponent_avg = calculate_opponent_average(
            player_logs,
            stat_column,
            opponent
        )

    recommendation, score, confidence, reasons = get_basic_recommendation(
        line,
        last_10_avg,
        season_avg,
        hit_rate,
        trend_direction,
        opponent_avg
    )

    return {
        "player": player_name,
        "stat": stat_type,
        "line": line,
        "opponent": opponent,
        "last_5_avg": last_5_avg,
        "last_10_avg": last_10_avg,
        "season_avg": season_avg,
        "trend": trend_value,
        "trend_direction": trend_direction,
        "hit_rate": hit_rate,
        "hits": hit_count,
        "games_checked": len(player_logs.head(10)),
        "home_avg": home_avg,
        "away_avg": away_avg,
        "opponent_avg": opponent_avg,
        "recommendation": recommendation,
        "score": score,
        "confidence": confidence,
        "reasons": reasons,

    }
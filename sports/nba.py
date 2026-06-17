from nba_api.stats.endpoints import playergamelog
from nba_api.stats.static import players

from analysis.historical_analysis import calculate_recent_averages, calculate_trend, calculate_hit_rate, \
    calculate_home_away_split, calculate_opponent_average
from analysis.recommendation_engine import get_basic_recommendation
from analysis.matchup_parser import parse_basketball_matchup

DEFAULT_SEASON = "2025-26"
DEFAULT_SEASON_TYPE = "Playoffs"

PLAYER_GAME_LOG_CACHE = {}

def find_player_id(player_name):
    matches = players.find_players_by_full_name(player_name)

    if not matches:
        return None

    return matches[0]["id"]

def add_calculated_stats(df):
    """
    Add PrizePicks-style stat columns that do not exist directly
    in the NBA API game log.

    Lo Note:
    PrizePicks uses stat labels like 3PM and PRA.
    The NBA API may store those stats under different column names
    or require us to calculate them.
    """
    if "FG3M" in df.columns:
        df["3PM"] = df["FG3M"]

    if "FG3A" in df.columns:
        df["3PTA"] = df["FG3A"]

    if "FGM" in df.columns and "FG3M" in df.columns:
        df["2PM"] = df["FGM"] - df["FG3M"]

    if all(column in df.columns for column in ["PTS", "REB", "AST"]):
        df["PRA"] = df["PTS"] + df["REB"] + df["AST"]

    if all(column in df.columns for column in ["REB", "AST"]):
        df["Rebs+Asts"] = df["REB"] + df["AST"]

    return df

def get_player_analysis(player_name,stat_type,line,opponent,season=DEFAULT_SEASON,season_type=DEFAULT_SEASON_TYPE):
    """
        Build a full statistical analysis for one player prop.

        This function is the "engine" of the historical stats module.

        It does NOT print anything.
        It collects the data, calculates the metrics, builds the recommendation,
        and returns everything as a dictionary so other parts of the app can use it.

        Lo Note:
        Keeping this function separate from the print/report functions makes it easier
        to reuse the same analysis later for rankings, parlays, dashboards, and tracking.
        """

    player_id = find_player_id(player_name)

    if player_id is None:
        return None

    cache_key = (
        player_id,
        season,
        season_type
    )

    if cache_key in PLAYER_GAME_LOG_CACHE:
        df = PLAYER_GAME_LOG_CACHE[cache_key]

    else:
        game_log = playergamelog.PlayerGameLog(
            player_id=player_id,
            season=season,
            season_type_all_star=season_type
        )

        df = game_log.get_data_frames()[0]
        df = add_calculated_stats(df)

        #print(player_name)
        #print(df[["GAME_DATE", "PTS", "REB", "AST", "PRA"]].head(10))

        PLAYER_GAME_LOG_CACHE[cache_key] = df


    if stat_type not in df.columns:
        print(f"Unsupported stat type skipped: {stat_type}")
        return None

    parsed_matchups = df["MATCHUP"].apply(parse_basketball_matchup)

    df["location"] = parsed_matchups.apply(lambda x: x[0])
    df["opponent"] = parsed_matchups.apply(lambda x: x[1])

    last_10 = df.head(10)

    if len(last_10) == 0:
        print(f"No game log data skipped: {player_name} {stat_type}")
        return None

    averages = calculate_recent_averages(df, stat_type)

    last_5_avg = averages["last_5_avg"]
    last_10_avg = averages["last_10_avg"]
    season_avg = averages["season_avg"]

    trend_data = calculate_trend(df, stat_type)

    trend = trend_data["trend_value"]
    trend_direction = trend_data["trend_direction"]

    hit_data = calculate_hit_rate(df, stat_type, line)

    hits = hit_data["hit_count"]
    hit_rate = hit_data["hit_rate"]

    home_away_data = calculate_home_away_split(
        df,
        stat_type,
        location_column="location"
    )

    home_avg = home_away_data["home_avg"]
    away_avg = home_away_data["away_avg"]

    opponent_avg = calculate_opponent_average(
        df,
        stat_type,
        opponent,
        opponent_column="opponent"
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
        "trend": trend,
        "trend_direction": trend_direction,
        "hit_rate": hit_rate,
        "hits": int(hits),
        "games_checked": len(last_10),
        "home_avg": home_avg,
        "away_avg": away_avg,
        "opponent_avg": opponent_avg,
        "recommendation": recommendation,
        "score": score,
        "confidence": confidence,
        "reasons": reasons
    }
import pandas as pd


def calculate_recent_averages(player_logs, stat_type):
    """
    Calculate recent averages for a player stat.

    This function is sport-agnostic.

    Requirements:
    - player_logs must already be filtered to one player.
    - player_logs must already be sorted with most recent games first.
    - stat_type must exist as a column in player_logs.

    Returns:
    - last_5_avg
    - last_10_avg
    - season_avg
    """

    last_5_avg = float(round(player_logs.head(5)[stat_type].mean(), 2))
    last_10_avg = float(round(player_logs.head(10)[stat_type].mean(), 2))
    season_avg = float(round(player_logs[stat_type].mean(), 2))

    return {
        "last_5_avg": last_5_avg,
        "last_10_avg": last_10_avg,
        "season_avg": season_avg,
    }

def calculate_hit_rate(player_logs, stat_type, line, sample_size=10):
    """
    Calculate hit rate against a prop line.

    Example:
    PRA > 35.5

    Returns:
    - hit_count
    - hit_rate
    """

    recent_games = player_logs.head(sample_size)

    hits = recent_games[
        recent_games[stat_type] > line
    ]

    hit_count = int(len(hits))

    hit_rate = float(round(
        (hit_count / len(recent_games)) * 100,
        2
    ))

    return {
        "hit_count": hit_count,
        "hit_rate": hit_rate
    }

def calculate_trend(player_logs, stat_type):
    """
    Calculate trend by comparing last 5 average to last 10 average.
    """

    last_5_avg = player_logs.head(5)[stat_type].mean()
    last_10_avg = player_logs.head(10)[stat_type].mean()

    trend_value = float(round(last_5_avg - last_10_avg, 2))

    if trend_value > 0:
        trend_direction = "UP"
    elif trend_value < 0:
        trend_direction = "DOWN"
    else:
        trend_direction = "FLAT"

    return {
        "trend_direction": trend_direction,
        "trend_value": trend_value
    }

def calculate_home_away_split(player_logs, stat_type, location_column="team_location"):
    """
    Calculate home and away averages for a player stat.

    Requirements:
    - player_logs must contain a location column.
    - location values should be "home" and "away".
    """

    if location_column not in player_logs.columns:
        return {
            "home_avg": None,
            "away_avg": None
        }

    home_games = player_logs[
        player_logs[location_column].str.lower() == "home"
    ]

    away_games = player_logs[
        player_logs[location_column].str.lower() == "away"
    ]

    home_avg = None
    away_avg = None

    if not home_games.empty:
        home_avg = float(round(home_games[stat_type].mean(), 2))

    if not away_games.empty:
        away_avg = float(round(away_games[stat_type].mean(), 2))

    return {
        "home_avg": home_avg,
        "away_avg": away_avg
    }

def calculate_opponent_average(player_logs, stat_type, opponent, opponent_column="opponent"):
    """
    Calculate a player's average for a stat against a specific opponent.

    Requirements:
    - player_logs must contain an opponent column.
    - opponent should match the abbreviation stored in that column.

    Returns:
    - opponent_avg
    """

    if opponent_column not in player_logs.columns:
        return "N/A"

    opponent_games = player_logs[
        player_logs[opponent_column] == opponent
    ]

    if opponent_games.empty:
        return "N/A"

    opponent_avg = float(round(opponent_games[stat_type].mean(), 2))

    return opponent_avg


def build_evidence_profile(
    player_logs,
    stat_type,
    opponent=None,
    recent_game_window=10,
    location_column="team_location",
    opponent_column="opponent",
    game_date_column="game_date",
    data_season=None,
):
    """
    Build factual metadata describing the evidence available
    for one player-stat analysis.

    This profile does not score, classify, or interpret evidence.
    It must not change recommendation or confidence behavior.
    """
    total_game_rows = int(len(player_logs))

    valid_stat_rows = int(
        player_logs[stat_type].notna().sum()
    )

    missing_stat_rows = int(
        player_logs[stat_type].isna().sum()
    )

    available_recent_game_count = int(
        len(player_logs.head(recent_game_window))
    )

    opponent_matchup_count = 0

    if (
        opponent is not None
        and opponent_column in player_logs.columns
    ):
        opponent_matchup_count = int(
            (player_logs[opponent_column] == opponent).sum()
        )

    home_game_count = 0
    away_game_count = 0

    if location_column in player_logs.columns:
        normalized_locations = (
            player_logs[location_column]
            .astype("string")
            .str.lower()
        )

        home_game_count = int(
            (normalized_locations == "home").sum()
        )

        away_game_count = int(
            (normalized_locations == "away").sum()
        )

    earliest_game_date = None
    latest_game_date = None

    if game_date_column in player_logs.columns:
        game_dates = pd.to_datetime(
            player_logs[game_date_column],
            errors="coerce",
        ).dropna()

        if not game_dates.empty:
            earliest_game_date = (
                game_dates.min().date().isoformat()
            )

            latest_game_date = (
                game_dates.max().date().isoformat()
            )

    return {
        "total_game_rows": total_game_rows,
        "valid_stat_rows": valid_stat_rows,
        "missing_stat_rows": missing_stat_rows,
        "requested_recent_game_window": recent_game_window,
        "available_recent_game_count": available_recent_game_count,
        "opponent_matchup_count": opponent_matchup_count,
        "home_game_count": home_game_count,
        "away_game_count": away_game_count,
        "earliest_game_date": earliest_game_date,
        "latest_game_date": latest_game_date,
        "data_season": data_season,
    }

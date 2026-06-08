from nba_api.stats.static import players
from nba_api.stats.endpoints import playergamelog

# ============================================================
# PLAYER LOOKUP FUNCTIONS
# ============================================================
def find_player_id(player_name):
    matches = players.find_players_by_full_name(player_name)

    if not matches:
        return None

    return matches[0]["id"]
# ============================================================
# HELPER FUNCTIONS
# ============================================================
def parse_matchup(matchup):
    if "@" in matchup:
        location = "Away"
    elif "vs." in matchup:
        location = "Home"
    else:
        location = "Unknown"

    opponent = matchup.split()[-1]

    return location, opponent

def get_hit_rate(player_name, stat_type, line):
    player_id = find_player_id(player_name)

    if player_id is None:
        print("Player not found.")
        return

    game_log = playergamelog.PlayerGameLog(
        player_id=player_id,
        season="2024-25",
        season_type_all_star="Regular Season"
    )

    df = game_log.get_data_frames()[0]

    last_10 = df.head(10)

    hits = (last_10[stat_type] > line).sum()

    hit_rate = round((hits / len(last_10)) * 100, 2)

    print(f"\n{player_name}")
    print(f"{stat_type} Line: {line}")
    print(f"Hit Rate Over: {hits}/{len(last_10)}")
    print(f"Hit Rate: {hit_rate}%")

def get_recent_averages(player_name, stat_type):
    player_id = find_player_id(player_name)

    if player_id is None:
        print("Player not found.")
        return

    game_log = playergamelog.PlayerGameLog(
        player_id=player_id,
        season="2024-25",
        season_type_all_star="Regular Season"
    )

    df = game_log.get_data_frames()[0]

    last_5_avg = round(df[stat_type].head(5).mean(), 2)
    last_10_avg = round(df[stat_type].head(10).mean(), 2)
    season_avg = round(df[stat_type].mean(), 2)

    print(f"\n{player_name}")
    print(f"{stat_type} Recent Averages")
    print("=" * 40)
    print(f"Last 5 Average: {last_5_avg}")
    print(f"Last 10 Average: {last_10_avg}")
    print(f"Season Average: {season_avg}")

def analyze_player_stat(player_name, stat_type, line):
    player_id = find_player_id(player_name)

    if player_id is None:
        print("Player not found.")
        return

    game_log = playergamelog.PlayerGameLog(
        player_id=player_id,
        season="2024-25",
        season_type_all_star="Regular Season"
    )

    df = game_log.get_data_frames()[0]

    last_5 = df.head(5)
    last_10 = df.head(10)

    last_5_avg = round(last_5[stat_type].mean(), 2)
    last_10_avg = round(last_10[stat_type].mean(), 2)
    season_avg = round(df[stat_type].mean(), 2)

    trend = round(last_5_avg - last_10_avg, 2)

    if trend > 0:
        trend_direction = "UP"
    elif trend < 0:
        trend_direction = "DOWN"
    else:
        trend_direction = "FLAT"

    hits = (last_10[stat_type] > line).sum()
    hit_rate = round((hits / len(last_10)) * 100, 2)

    print(f"\n{player_name}")
    print("=" * 40)
    print(f"Stat: {stat_type}")
    print(f"Line: {line}")
    print()
    print(f"Last 5 Average: {last_5_avg}")
    print(f"Last 10 Average: {last_10_avg}")
    print(f"Season Average: {season_avg}")
    print()
    print(f"Trend: {trend_direction} ({trend})")
    print()
    print(f"Hit Rate Over {line}: {hits}/{len(last_10)}")
    print(f"Hit Rate: {hit_rate}%")

def show_clean_game_log(player_name):
    player_id = find_player_id(player_name)

    if player_id is None:
        print("Player not found.")
        return

    game_log = playergamelog.PlayerGameLog(
        player_id=player_id,
        season="2024-25",
        season_type_all_star="Regular Season"
    )

    df = game_log.get_data_frames()[0]

    parsed_matchups = df["MATCHUP"].apply(parse_matchup)

    df["location"] = parsed_matchups.apply(lambda x: x[0])
    df["opponent"] = parsed_matchups.apply(lambda x: x[1])

    print(df[["GAME_DATE", "MATCHUP", "location", "opponent", "PTS", "REB", "AST"]].head(10).to_string(index=False))

def get_home_away_split(player_name, stat_type):
    player_id = find_player_id(player_name)

    if player_id is None:
        print("Player not found.")
        return

    game_log = playergamelog.PlayerGameLog(
        player_id=player_id,
        season="2024-25",
        season_type_all_star="Regular Season"
    )

    df = game_log.get_data_frames()[0]

    parsed_matchups = df["MATCHUP"].apply(parse_matchup)

    df["location"] = parsed_matchups.apply(lambda x: x[0])
    df["opponent"] = parsed_matchups.apply(lambda x: x[1])

    home_games = df[df["location"] == "Home"]
    away_games = df[df["location"] == "Away"]

    home_avg = round(home_games[stat_type].mean(), 2)
    away_avg = round(away_games[stat_type].mean(), 2)

    print(f"\n{player_name}")
    print("=" * 40)
    print(f"{stat_type} Home/Away Split")
    print()
    print(f"Home Games: {len(home_games)}")
    print(f"Home Average: {home_avg}")
    print()
    print(f"Away Games: {len(away_games)}")
    print(f"Away Average: {away_avg}")

def get_opponent_average(player_name, stat_type, opponent):
    player_id = find_player_id(player_name)

    if player_id is None:
        print("Player not found.")
        return

    game_log = playergamelog.PlayerGameLog(
        player_id=player_id,
        season="2024-25",
        season_type_all_star="Regular Season"
    )

    df = game_log.get_data_frames()[0]

    parsed_matchups = df["MATCHUP"].apply(parse_matchup)

    df["location"] = parsed_matchups.apply(lambda x: x[0])
    df["opponent"] = parsed_matchups.apply(lambda x: x[1])

    opponent_games = df[df["opponent"] == opponent]

    if opponent_games.empty:
        print(f"\nNo games found against {opponent}.")
        return

    opponent_avg = round(opponent_games[stat_type].mean(), 2)

    print(f"\n{player_name}")
    print("=" * 40)
    print(f"{stat_type} vs {opponent}")
    print()
    print(f"Games Found: {len(opponent_games)}")
    print(f"Average: {opponent_avg}")
# ============================================================
# RECOMMENDATION ENGINE
# ============================================================
def get_basic_recommendation(


    line,
    last_10_avg,
    season_avg,
    hit_rate,
    trend_direction,
    opponent_avg
):
    """
    Generate a recommendation, confidence level, and reasoning.

    Scoring System:
    +1 = Positive indicator
    -1 = Negative indicator

    Indicators:
    - Last 10 average
    - Season average
    - Hit rate
    - Recent trend
    - Opponent history

    Lo Note:
    This is the heart of the recommendation engine.
    Any future improvements to recommendation quality will likely
    happen inside this function.
    """
    score = 0
    reasons = []

    if last_10_avg > line:
        score += 1
        reasons.append("Last 10 average is above the line.")
    else:
        score -= 1
        reasons.append("Last 10 average is below the line.")

    if season_avg > line:
        score += 1
        reasons.append("Season average is above the line.")
    else:
        score -= 1
        reasons.append("Season average is below the line.")

    if hit_rate >= 60:
        score += 1
        reasons.append("Hit rate is 60% or higher.")
    elif hit_rate <= 50:
        score -= 1
        reasons.append("Hit rate is 50% or lower.")

    if trend_direction == "UP":
        score += 1
        reasons.append("Recent trend is up.")
    elif trend_direction == "DOWN":
        score -= 1
        reasons.append("Recent trend is down.")

    if opponent_avg != "N/A":
        if opponent_avg > line:
            score += 1
            reasons.append("Opponent average is above the line.")
        else:
            score -= 1
            reasons.append("Opponent average is below the line.")

    if score >= 4:
        recommendation = "STRONG MORE"
    elif score >= 2:
        recommendation = "LEAN MORE"
    elif score <= -4:
        recommendation = "STRONG LESS"
    elif score <= -2:
        recommendation = "LEAN LESS"
    else:
        recommendation = "PASS"

    if score >= 4:
        confidence = "HIGH"
    elif score >= 2:
        confidence = "MEDIUM"
    else:
        confidence = "LOW"

    return recommendation, score, confidence,  reasons

# ============================================================
# CORE ANALYSIS ENGINE
# ============================================================

def get_player_analysis(player_name, stat_type, line, opponent):
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

    game_log = playergamelog.PlayerGameLog(
        player_id=player_id,
        season="2024-25",
        season_type_all_star="Regular Season"
    )

    df = game_log.get_data_frames()[0]

    parsed_matchups = df["MATCHUP"].apply(parse_matchup)

    df["location"] = parsed_matchups.apply(lambda x: x[0])
    df["opponent"] = parsed_matchups.apply(lambda x: x[1])

    last_5 = df.head(5)
    last_10 = df.head(10)

    last_5_avg = round(last_5[stat_type].mean(), 2)
    last_10_avg = round(last_10[stat_type].mean(), 2)
    season_avg = round(df[stat_type].mean(), 2)

    trend = round(last_5_avg - last_10_avg, 2)

    if trend > 0:
        trend_direction = "UP"
    elif trend < 0:
        trend_direction = "DOWN"
    else:
        trend_direction = "FLAT"

    hits = (last_10[stat_type] > line).sum()
    hit_rate = round((hits / len(last_10)) * 100, 2)

    home_avg = round(df[df["location"] == "Home"][stat_type].mean(), 2)
    away_avg = round(df[df["location"] == "Away"][stat_type].mean(), 2)

    opponent_games = df[df["opponent"] == opponent]

    if len(opponent_games) > 0:
        opponent_avg = round(opponent_games[stat_type].mean(), 2)
    else:
        opponent_avg = "N/A"

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

# ============================================================
# REPORT / DISPLAY FUNCTIONS
# ============================================================

def analyze_player_stat_full(player_name, stat_type, line, opponent):
    """
    Print a readable full analysis report for one player prop.

    This function uses get_player_analysis() to do the math, then handles
    the user-facing display.

    Why:
    We do not want this function recalculating stats. Its only job is to
    format and print the analysis in a way that is easy to read.
    """
    analysis = get_player_analysis(player_name, stat_type, line, opponent)

    if analysis is None:
        print("Player not found.")
        return

    print(f"\n{analysis['player']}")
    print("=" * 50)
    print(f"Stat: {analysis['stat']}")
    print(f"Line: {analysis['line']}")
    print(f"Opponent: {analysis['opponent']}")
    print()
    print(f"Last 5 Average: {analysis['last_5_avg']}")
    print(f"Last 10 Average: {analysis['last_10_avg']}")
    print(f"Season Average: {analysis['season_avg']}")
    print()
    print(f"Trend: {analysis['trend_direction']} ({analysis['trend']})")
    print()
    print(
        f"Hit Rate Over {analysis['line']}: "
        f"{analysis['hits']}/{analysis['games_checked']}"
    )
    print(f"Hit Rate: {analysis['hit_rate']}%")
    print()
    print(f"Home Average: {analysis['home_avg']}")
    print(f"Away Average: {analysis['away_avg']}")
    print()
    print(
        f"{analysis['stat']} Average vs "
        f"{analysis['opponent']}: {analysis['opponent_avg']}"
    )
    print()
    print(f"Recommendation: {analysis['recommendation']}")
    print(f"Recommendation Score: {analysis['score']}")
    print(f"Confidence: {analysis['confidence']}")
    print("Reasons:")

    for reason in analysis["reasons"]:
        print(f"- {reason}")

#get_hit_rate("Jalen Brunson", "PTS", 25.5)
#get_recent_averages("Jalen Brunson", "PTS")
#analyze_player_stat("Jalen Brunson", "PTS", 25.5)
#show_clean_game_log("Jalen Brunson")
#get_home_away_split("Jalen Brunson", "PTS")
#get_opponent_average("Jalen Brunson", "PTS", "BOS")
analyze_player_stat_full("Jalen Brunson", "PTS", 25.5, "BOS")
#analysis = get_player_analysis("Jalen Brunson", "PTS", 25.5, "BOS")
#print(analysis)


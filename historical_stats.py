from datetime import datetime
import csv
import pandas as pd
from nba_api.stats.static import players
from nba_api.stats.endpoints import playergamelog

PLAYER_GAME_LOG_CACHE = {}

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

    if abs(score) >= 4:
        confidence = "HIGH"
    elif abs(score) >= 2:
        confidence = "MEDIUM"
    else:
        confidence = "LOW"

    return recommendation, score, confidence,  reasons

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

    return df

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

    if player_id in PLAYER_GAME_LOG_CACHE:
        df = PLAYER_GAME_LOG_CACHE[player_id]
    else:
        game_log = playergamelog.PlayerGameLog(
            player_id=player_id,
            season="2024-25",
            season_type_all_star="Regular Season"
        )

        df = game_log.get_data_frames()[0]
        df = add_calculated_stats(df)

        PLAYER_GAME_LOG_CACHE[player_id] = df


    if stat_type not in df.columns:
        print(f"Unsupported stat type skipped: {stat_type}")
        return None

    parsed_matchups = df["MATCHUP"].apply(parse_matchup)

    df["location"] = parsed_matchups.apply(lambda x: x[0])
    df["opponent"] = parsed_matchups.apply(lambda x: x[1])

    last_5 = df.head(5)
    last_10 = df.head(10)

    if len(last_10) == 0:
        print(f"No game log data skipped: {player_name} {stat_type}")
        return None

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

# ============================================================
# PROP COMPARISON / RANKING FUNCTIONS
# ============================================================
def compare_props(props):
    """
    Analyze and rank multiple player props.

    Each prop should be a tuple in this format:

    (player_name, stat_type, line, opponent)

    Example:
    ("Jalen Brunson", "PTS", 25.5, "BOS")

    Why:
    This is the first step toward ranking opportunities and eventually
    building suggested slips/parlays.
    """
    results = []

    game_log_cache = {}

    for prop in props:
        player_name, stat_type, line, opponent, game_date, risk_type = prop

        analysis = get_player_analysis(
            player_name,
            stat_type,
            line,
            opponent
        )

        if analysis is not None:
            analysis["risk_type"] = risk_type
            analysis["game_date"] = game_date

            # Lo Note:
            # Goblin and Demon props are MORE-only on PrizePicks.
            # If the engine recommends LESS for one of these, convert it to PASS
            # because LESS is not a playable option.
            if risk_type in ["GOBLIN", "DEMON"]:
                if analysis["recommendation"] in ["LEAN LESS", "STRONG LESS"]:
                    analysis["recommendation"] = "PASS"
                    analysis["confidence"] = "LOW"
            results.append(analysis)

    # Lo Note:
    # Props are ranked primarily by recommendation score.
    # If two props have the same score, the higher hit rate
    # wins the tie-breaker.
    #
    # Example:
    # Score 1, Hit Rate 80%
    # beats
    # Score 1, Hit Rate 50%

    ranked_results = sorted(
        results,
        key=lambda item: (
            item["score"],
            item["hit_rate"]
        ),
        reverse=True
    )

    strong_more_count = sum(
        1 for item in ranked_results
        if item["recommendation"] == "STRONG MORE"
    )

    lean_more_count = sum(
        1 for item in ranked_results
        if item["recommendation"] == "LEAN MORE"
    )

    pass_count = sum(
        1 for item in ranked_results
        if item["recommendation"] == "PASS"
    )

    lean_less_count = sum(
        1 for item in ranked_results
        if item["recommendation"] == "LEAN LESS"
    )

    strong_less_count = sum(
        1 for item in ranked_results
        if item["recommendation"] == "STRONG LESS"
    )

    goblin_count = sum(
        1 for item in ranked_results
        if item["risk_type"] == "GOBLIN"
    )

    normal_count = sum(
        1 for item in ranked_results
        if item["risk_type"] == "NORMAL"
    )

    demon_count = sum(
        1 for item in ranked_results
        if item["risk_type"] == "DEMON"
    )

    print()
    print("=" * 90)
    print("PROP COMPARISON REPORT")
    print("=" * 90)
    print("SUMMARY")
    print("-" * 90)
    print(f"STRONG MORE : {strong_more_count}")
    print(f"LEAN MORE   : {lean_more_count}")
    print(f"PASS        : {pass_count}")
    print(f"LEAN LESS   : {lean_less_count}")
    print(f"STRONG LESS : {strong_less_count}")
    print("-" * 90)
    print("RISK BREAKDOWN")
    print("-" * 90)
    print(f"GOBLIN : {goblin_count}" )
    print(f"NORMAL : {normal_count}")
    print(f"DEMON  : {demon_count}")
    print("=" * 90)


    #===================
    # Header
    #==================
    print(
        f"{'#':<4} "
        f"{'Player':<22} "
        f"{'Stat':<6} "
        f"{'Line':<7} "
        f"{'Risk':<8} "
        f"{'Opp':<5} "
        f"{'Score':<6} "
        f"{'Hit%':<8} "
        f"{'Rec':<15} "
        f"{'Conf'}"
    )

    print("-" * 90)

    for rank, item in enumerate(ranked_results, start=1):
        #=========================
        # Rows
        #==========================
        print(
            f"{rank:<4} "
            f"{item['player']:<22} "
            f"{item['stat']:<6} "
            f"{item['line']:<7} "
            f"{item['risk_type']:<8} "
            f"{item['opponent']:<5} "
            f"{item['score']:<6} "
            f"{str(round(item['hit_rate'], 1)) + '%':<8} "
            f"{item['recommendation']:<15} "
            f"{item['confidence']}"
        )

    print("-" * 90)

    print("MORE-SIDE OPPORTUNITIES")

    top_opportunities = [
        item for item in ranked_results
        if item["recommendation"] in ["STRONG MORE", "LEAN MORE"]
    ]

    if top_opportunities:
        for rank, item in enumerate(top_opportunities, start=1):
            print(
                f"{rank}. {item['player']} | "
                f"{item['stat']} {item['line']} vs {item['opponent']} | "
                f"{item['recommendation']} | "
                f"Score: {item['score']} | "
                f"Confidence: {item['confidence']}"
            )
    else:
        print("No MORE-side opportunities found.")

    print("-" * 90)

    print("LESS-SIDE OPPORTUNITIES")

    fade_opportunities = [
        item for item in ranked_results
        if item["recommendation"] in ["STRONG LESS", "LEAN LESS"]
    ]

    if fade_opportunities:
        for rank, item in enumerate(fade_opportunities, start=1):
            print(
                f"{rank}. {item['player']} | "
                f"{item['stat']} {item['line']} vs {item['opponent']} | "
                f"{item['recommendation']} | "
                f"Score: {item['score']} | "
                f"Confidence: {item['confidence']}"
            )
    else:
        print("No LESS-side opportunities found.")

    print("-" * 90)

    best_play = ranked_results[0]

    if best_play["recommendation"] != "PASS":
        print("BEST AVAILABLE PLAY")
        print(
            f"{best_play['player']} | "
            f"{best_play['stat']} {best_play['line']} vs {best_play['opponent']} | "
            f"{best_play['recommendation']} | "
            f"Score: {best_play['score']} | "
            f"Confidence: {best_play['confidence']}"
        )
    else:
        print("BEST AVAILABLE PLAY")
        print("No playable MORE recommendation found. Top-ranked prop is still a PASS.")

    print("-" * 90)
    print("TOP ACTIONABLE OPPORTUNITY DETAILS")
    print("-" * 90)

    detail_prop = None

    if top_opportunities:
        detail_prop = top_opportunities[0]
    elif fade_opportunities:
        detail_prop = fade_opportunities[0]
    elif ranked_results:
        detail_prop = ranked_results[0]

    if detail_prop is not None:
        print(
            f"{detail_prop['player']} | "
            f"{detail_prop['stat']} {detail_prop['line']} vs "
            f"{detail_prop['opponent']} | "
            f"{detail_prop['recommendation']} | "
            f"Confidence: {detail_prop['confidence']}"
        )

        print()
        print("Reasons:")

        for reason in detail_prop["reasons"]:
            print(f"- {reason}")
    else:
        print("No prop details available.")

    return ranked_results

# ============================================================
# FILE INPUT FUNCTIONS
# ============================================================
def load_props_from_csv(file_path):
    """
    Load prop data from a CSV file.

    Expected Format:

    player,stat,line,opponent
    Jalen Brunson,PTS,25.5,BOS

    Lo Note:
    This is the first step toward user-managed prop lists and
    eventually PrizePicks board imports.
    """
    props = []

    with open(file_path, newline="", encoding="utf-8") as csvfile:
        reader = csv.DictReader(csvfile)

        for row in reader:
            props.append(
                (
                    row["player"],
                    row["stat"],
                    float(row["line"]),
                    row["opponent"],
                    row["game_date"],
                    row["risk_type"]
                )
            )

    return props

def determine_result(recommendation, line, actual_stat):
    """
    Determine whether a paper bet won, lost, pushed, or should be ignored.

    Lo Note:
    MORE recommendations win when the actual stat is greater than the line.
    LESS recommendations win when the actual stat is less than the line.
    PASS recommendations are not graded.
    """
    if recommendation == "PASS":
        return "PASS"

    if actual_stat == line:
        return "PUSH"

    if recommendation in ["STRONG MORE", "LEAN MORE"]:
        if actual_stat > line:
            return "WIN"
        return "LOSS"

    if recommendation in ["STRONG LESS", "LEAN LESS"]:
        if actual_stat < line:
            return "WIN"
        return "LOSS"

    return "UNKNOWN"

# ============================================================
# PAPER BET TRACKING FUNCTIONS
# ============================================================
def save_paper_bet(prop):
    """
    Save a paper bet recommendation to paper_bets.csv.

    Lo Note:
    This is the beginning of engine validation.
    Every recommendation saved here can later be
    graded as WIN, LOSS, or PUSH.
    """

    if paper_bet_exists(prop):
        print(
            f"Skipping duplicate: "
            f"{prop['player']} "
            f"{prop['stat']} "
            f"{prop['line']} "
            f"{prop['risk_type']}"
        )
        return False

    with open("paper_bets.csv", "a", newline="", encoding="utf-8") as file:
        writer = csv.writer(file)

        writer.writerow([
            datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            prop["game_date"],
            prop["player"],
            prop["stat"],
            prop["line"],
            prop["opponent"],
            prop["risk_type"],
            prop["recommendation"],
            prop["confidence"],
            "PENDING",
            ""
        ])

        return True

def save_recommendations_to_paper_bets(results):
    """
    Save all analyzed props to paper_bets.csv.

    Lo Note:
    This allows an entire board of props to be saved
    at once for paper betting and future engine analysis.
    """

    print()
    print("-" * 90)
    print("PAPER BET SAVE RESULTS")
    print("-" * 90)

    saved_count = 0
    skipped_count = 0

    for prop in results:
        if save_paper_bet(prop):
            saved_count += 1
        else:
            skipped_count += 1

    print()
    print(f"New recommendations saved: {saved_count}")
    print(f"Duplicates skipped: {skipped_count}")

def paper_bet_exists(prop):
    """
    Check if a paper bet already exists.

    Duplicate Key:
    - game_date
    - player
    - stat
    - line
    - risk_type

    Lo Note:
    We intentionally do NOT use timestamp because
    the same prop may be analyzed multiple times.
    """

    with open("paper_bets.csv", "r", newline="", encoding="utf-8") as file:
        reader = csv.DictReader(file)

        for row in reader:

            if (
                row["game_date"] == prop["game_date"]
                and row["player"] == prop["player"]
                and row["stat"] == prop["stat"]
                and float(row["line"]) == float(prop["line"])
                and row["risk_type"] == prop["risk_type"]
            ):
                return True

    return False

def update_paper_bet_results():
    df = pd.read_csv("paper_bets.csv")

    while True:
        pending_bets = df[
            (df["result"] == "PENDING") &
            (df["recommendation"] != "PASS")
        ]

        if pending_bets.empty:
            print("No pending actionable bets to update.")
            break

        print()
        print("PENDING BETS")
        print("-" * 90)

        for index, row in pending_bets.iterrows():
            print(
                f"{index}: "
                f"{row['player']} "
                f"{row['stat']} "
                f"{row['line']} "
                f"{row['recommendation']}"
            )

        selected_index = int(input("Enter the index number to update: "))


        selected_row = df.loc[selected_index]

        print()
        print("SELECTED BET")
        print("-" * 90)
        print(
            f"{selected_row['player']} | "
            f"{selected_row['stat']} {selected_row['line']} | "
            f"{selected_row['recommendation']} | "
            f"Risk: {selected_row['risk_type']}"
        )

        actual_stat = float(input("Enter the actual stat: "))

        new_result = determine_result(
            selected_row["recommendation"],
            float(selected_row["line"]),
            actual_stat
        )

        df.loc[selected_index, "actual_stat"] = str(actual_stat)
        df.loc[selected_index, "result"] = new_result

        df.to_csv("paper_bets.csv", index=False)

        print()
        print(
            f"Updated {selected_row['player']} "
            f"{selected_row['stat']} {selected_row['line']} "
            f"as {new_result}"
        )

        update_again = input("Update another bet? Y//N: ").strip().upper()

        if update_again != "Y":
            print("Finished updating paper bets.")
            break

    show_engine_record()

def show_engine_record():
    """
    Display the current engine record from paper_bets.csv.
    """

    df = pd.read_csv("paper_bets.csv")

    wins = len(df[df["result"] == "WIN"])
    losses = len(df[df["result"] == "LOSS"])
    pushes = len(df[df["result"] == "PUSH"])
    pending = len(
        df[
            (df["result"] == "PENDING") &
            (df["recommendation"] != "PASS")
        ]
    )

    total_graded = wins + losses + pushes

    if total_graded > 0:
        win_rate = round((wins / total_graded) * 100, 2)
    else:
        win_rate = 0

    print()
    print("-" * 90)
    print("ENGINE RECORD")
    print("-" * 90)
    print(f"Wins: {wins}")
    print(f"Losses: {losses}")
    print(f"Pushes: {pushes}")
    print(f"Pending: {pending}")
    print(f"Win Rate: {win_rate}%")

def show_recommendation_breakdown():
    """
    Display performance by recommendation type.
    """
    df = pd.read_csv("paper_bets.csv")

    recommendation_types = [
        "STRONG MORE",
        "LEAN MORE",
        "STRONG LESS",
        "LEAN LESS"
    ]

    print()
    print("-" * 90)
    print("RECOMMENDATION BREAKDOWN")
    print("-" * 90)

    for recommendation in recommendation_types:
        recommendation_df = df[df["recommendation"] == recommendation]

        wins = len(recommendation_df[recommendation_df["result"] == "WIN"])
        losses = len(recommendation_df[recommendation_df["result"] == "LOSS"])
        pushes = len(recommendation_df[recommendation_df["result"] == "PUSH"])

        total_graded = wins + losses + pushes
        win_rate = round((wins / total_graded) * 100, 2) if total_graded > 0 else 0

        print()
        print(recommendation)
        print(f"Wins: {wins}")
        print(f"Losses: {losses}")
        print(f"Pushes: {pushes}")
        print(f"Win Rate: {win_rate}%")


def show_confidence_breakdown():
    """
    Display performance by confidence level.
    """
    df = pd.read_csv("paper_bets.csv")

    confidence_levels = [
        "HIGH",
        "MEDIUM",
        "LOW"
    ]

    print()
    print("-" * 90)
    print("CONFIDENCE BREAKDOWN")
    print("-" * 90)

    for confidence in confidence_levels:
        confidence_df = df[df["confidence"] == confidence]

        wins = len(confidence_df[confidence_df["result"] == "WIN"])
        losses = len(confidence_df[confidence_df["result"] == "LOSS"])
        pushes = len(confidence_df[confidence_df["result"] == "PUSH"])

        total_graded = wins + losses + pushes
        win_rate = round((wins / total_graded) * 100, 2) if total_graded > 0 else 0

        print()
        print(confidence)
        print(f"Wins: {wins}")
        print(f"Losses: {losses}")
        print(f"Pushes: {pushes}")
        print(f"Win Rate: {win_rate}%")


def show_risk_breakdown():
    """
    Display performance by risk type.
    """
    df = pd.read_csv("paper_bets.csv")

    risk_types = [
        "GOBLIN",
        "NORMAL",
        "DEMON"
    ]

    print()
    print("-" * 90)
    print("RISK BREAKDOWN")
    print("-" * 90)

    for risk_type in risk_types:
        risk_df = df[df["risk_type"] == risk_type]

        wins = len(risk_df[risk_df["result"] == "WIN"])
        losses = len(risk_df[risk_df["result"] == "LOSS"])
        pushes = len(risk_df[risk_df["result"] == "PUSH"])

        total_graded = wins + losses + pushes
        win_rate = round((wins / total_graded) * 100, 2) if total_graded > 0 else 0

        print()
        print(risk_type)
        print(f"Wins: {wins}")
        print(f"Losses: {losses}")
        print(f"Pushes: {pushes}")
        print(f"Win Rate: {win_rate}%")


def show_full_performance_report():
    """
    Display all engine performance reports.
    """
    show_engine_record()
    show_recommendation_breakdown()
    show_confidence_breakdown()
    show_risk_breakdown()
# ============================================================
# LEGACY DEVELOPMENT TESTS
# ============================================================
#get_hit_rate("Jalen Brunson", "PTS", 25.5)
#get_recent_averages("Jalen Brunson", "PTS")
#analyze_player_stat("Jalen Brunson", "PTS", 25.5)
#show_clean_game_log("Jalen Brunson")
#get_home_away_split("Jalen Brunson", "PTS")
#get_opponent_average("Jalen Brunson", "PTS", "BOS")
#analyze_player_stat_full("Jalen Brunson", "PTS", 25.5, "BOS")
#analysis = get_player_analysis("Jalen Brunson", "PTS", 25.5, "BOS")
#print(analysis)
#props_to_compare = [
 #   ("Jalen Brunson", "PTS", 25.5, "BOS"),
  #  ("Anthony Edwards", "REB", 6.5, "DEN"),
#]

#compare_props(props_to_compare)

# ============================================================
# TESTING
# ============================================================

# Lo Note:
# We are currently loading props from a CSV file.
# This replaces hardcoded test props and moves us one step
# closer to real-world usage.
#
# Future Evolution:
# CSV -> UI Form -> Automated Board Import


# ============================================================
# PAPER BETTING TEST WORKFLOW
# ============================================================

# Lo Note:
# Current workflow:
#
# 1. Load props from props.csv
# 2. Analyze props
# 3. Generate ranked report
# 4. Save recommendations to paper_bets.csv
#
# Future Evolution:
# CSV -> UI -> Automated Board Import
# Manual Save -> Menu Option -> UI Button
#props_to_compare = load_props_from_csv("props.csv")

#ranked_results = compare_props(props_to_compare)

#save_recommendations_to_paper_bets(ranked_results)


#update_paper_bet_results()


#show_recommendation_breakdown()

#show_confidence_breakdown()

#show_full_performance_report()

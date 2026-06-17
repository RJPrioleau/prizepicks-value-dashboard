import csv
import pandas as pd
from nba_api.stats.endpoints import playergamelog
from sports.nba import (
    find_player_id,
    get_player_analysis
)
from analysis.matchup_parser import parse_basketball_matchup


PLAYER_GAME_LOG_CACHE = {}


# ============================================================
# Utility / Debug Display
# ============================================================

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

    parsed_matchups = df["MATCHUP"].apply(parse_basketball_matchup)

    df["location"] = parsed_matchups.apply(lambda x: x[0])
    df["opponent"] = parsed_matchups.apply(lambda x: x[1])

    print(df[["GAME_DATE", "MATCHUP", "location", "opponent", "PTS", "REB", "AST"]].head(10).to_string(index=False))

# ============================================================
# Single Prop Analysis Display
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
# Prop Loading
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

# ============================================================
# Multi-Prop Comparison / Ranking
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
# Performance Reports
# ============================================================

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
# Diagnostic Reports
# ============================================================

def show_slate_breakdown():
    df = pd.read_csv("paper_bets.csv")
    dates = sorted(df["game_date"].unique())

    print()
    print("-" * 90)
    print("SLATE BREAKDOWN")
    print("-" * 90)

    for date in dates:
        slate_df = df[
            (df["game_date"] == date) &
            (df["recommendation"] != "PASS")
            ]

        wins = len(slate_df[slate_df["result"] == "WIN"])
        losses = len(slate_df[slate_df["result"] == "LOSS"])
        pushes = len(slate_df[slate_df["result"] == "PUSH"])

        total_graded = wins + losses + pushes

        if total_graded > 0:
            win_rate = round((wins / total_graded) * 100, 2)
        else:
            win_rate = 0

        print()
        print(date)
        print(f"Wins: {wins}")
        print(f"Losses: {losses}")
        print(f"Pushes: {pushes}")
        print(f"Win Rate: {win_rate}%")

def show_recommendation_breakdown_by_slate():
    df = pd.read_csv("paper_bets.csv")

    dates = sorted(df["game_date"].unique())

    recommendation_types = [
        "STRONG MORE",
        "LEAN MORE",
        "STRONG LESS",
        "LEAN LESS"
    ]

    print()
    print("-" * 90)
    print("RECOMMENDATION BREAKDOWN BY SLATE")
    print("-" * 90)

    for date in dates:
        print()
        print(date)
        print("-" * 40)

        slate_df = df[
            (df["game_date"] == date) &
            (df["recommendation"] != "PASS")
        ]

        for recommendation in recommendation_types:
            recommendation_df = slate_df[
                slate_df["recommendation"] == recommendation
            ]

            wins = len(recommendation_df[recommendation_df["result"] == "WIN"])
            losses = len(recommendation_df[recommendation_df["result"] == "LOSS"])
            pushes = len(recommendation_df[recommendation_df["result"] == "PUSH"])

            total_graded = wins + losses + pushes

            if total_graded > 0:
                win_rate = round((wins / total_graded) * 100, 2)
            else:
                win_rate = 0

            print(
                f"{recommendation}: "
                f"{wins}-{losses}-{pushes} | "
                f"Win Rate: {win_rate}%"
            )

def show_strong_more_by_risk_and_slate():
    df = pd.read_csv("paper_bets.csv")

    dates = sorted(df["game_date"].unique())

    risk_types = [
        "GOBLIN",
        "NORMAL",
        "DEMON"
    ]

    print()
    print("-" * 90)
    print("STRONG MORE BY RISK AND SLATE")
    print("-" * 90)

    for date in dates:
        print()
        print(date)
        print("-" * 40)

        slate_df = df[
            (df["game_date"] == date) &
            (df["recommendation"] == "STRONG MORE")
        ]

        for risk_type in risk_types:
            risk_df = slate_df[
                slate_df["risk_type"] == risk_type
            ]

            wins = len(risk_df[risk_df["result"] == "WIN"])
            losses = len(risk_df[risk_df["result"] == "LOSS"])
            pushes = len(risk_df[risk_df["result"] == "PUSH"])

            total_graded = wins + losses + pushes

            if total_graded > 0:
                win_rate = round((wins / total_graded) * 100, 2)
            else:
                win_rate = 0

            print(
                f"{risk_type}: "
                f"{wins}-{losses}-{pushes} | "
                f"Win Rate: {win_rate}%"
            )

def show_confidence_breakdown_by_slate():
    """
    Display confidence performance grouped by slate date.

    Lo Note:
    This helps us see whether HIGH confidence is actually
    outperforming MEDIUM confidence on each individual slate.
    """

    df = pd.read_csv("paper_bets.csv")

    dates = sorted(df["game_date"].unique())

    confidence_levels = [
        "HIGH",
        "MEDIUM",
        "LOW"
    ]

    print()
    print("-" * 90)
    print("CONFIDENCE BREAKDOWN BY SLATE")
    print("-" * 90)

    for date in dates:
        print()
        print(date)
        print("-" * 40)

        slate_df = df[
            (df["game_date"] == date) &
            (df["recommendation"] != "PASS")
        ]

        for confidence in confidence_levels:
            confidence_df = slate_df[
                slate_df["confidence"] == confidence
            ]

            wins = len(confidence_df[confidence_df["result"] == "WIN"])
            losses = len(confidence_df[confidence_df["result"] == "LOSS"])
            pushes = len(confidence_df[confidence_df["result"] == "PUSH"])

            total_graded = wins + losses + pushes

            if total_graded > 0:
                win_rate = round((wins / total_graded) * 100, 2)
            else:
                win_rate = 0

            print(
                f"{confidence}: "
                f"{wins}-{losses}-{pushes} | "
                f"Win Rate: {win_rate}%"
            )

def show_high_confidence_breakdown_by_recommendation():
    """
    Display HIGH confidence performance grouped by recommendation type.

    Lo Note:
    HIGH confidence is currently underperforming badly.

    Investigation Goal:
    Determine whether HIGH confidence failures are concentrated in:

    - STRONG MORE
    - STRONG LESS
    - LEAN MORE
    - LEAN LESS

    before making any changes to the scoring system.
    """

    df = pd.read_csv("paper_bets.csv")

    recommendation_types = [
        "STRONG MORE",
        "LEAN MORE",
        "LEAN LESS",
        "STRONG LESS"
    ]

    print()
    print("-" * 90)
    print("HIGH CONFIDENCE BREAKDOWN BY RECOMMENDATION")
    print("-" * 90)

    high_df = df[
        (df["confidence"] == "HIGH") &
        (df["recommendation"] != "PASS")
    ]

    for recommendation in recommendation_types:

        recommendation_df = high_df[
            high_df["recommendation"] == recommendation
        ]

        wins = len(
            recommendation_df[
                recommendation_df["result"] == "WIN"
            ]
        )

        losses = len(
            recommendation_df[
                recommendation_df["result"] == "LOSS"
            ]
        )

        pushes = len(
            recommendation_df[
                recommendation_df["result"] == "PUSH"
            ]
        )

        total_graded = wins + losses + pushes

        if total_graded > 0:
            win_rate = round(
                (wins / total_graded) * 100,
                2
            )
        else:
            win_rate = 0

        print(
            f"{recommendation}: "
            f"{wins}-{losses}-{pushes} | "
            f"Win Rate: {win_rate}%"
        )

def show_strong_more_by_risk_type():
    """
    Display STRONG MORE performance grouped by risk type.

    Lo Note:
    HIGH confidence failures are mostly STRONG MORE plays.
    This report helps determine whether the issue is tied to
    a specific risk type before changing scoring logic.
    """

    df = pd.read_csv("paper_bets.csv")

    strong_more_df = df[
        (df["recommendation"] == "STRONG MORE") &
        (df["result"] != "PASS")
    ]

    risk_types = sorted(strong_more_df["risk_type"].unique())

    print()
    print("-" * 90)
    print("STRONG MORE PERFORMANCE BY RISK TYPE")
    print("-" * 90)

    for risk_type in risk_types:
        risk_df = strong_more_df[
            strong_more_df["risk_type"] == risk_type
        ]

        wins = len(risk_df[risk_df["result"] == "WIN"])
        losses = len(risk_df[risk_df["result"] == "LOSS"])
        pushes = len(risk_df[risk_df["result"] == "PUSH"])

        total_graded = wins + losses + pushes

        if total_graded > 0:
            win_rate = round((wins / total_graded) * 100, 2)
        else:
            win_rate = 0

        print(
            f"{risk_type}: "
            f"{wins}-{losses}-{pushes} | "
            f"Win Rate: {win_rate}%"
        )

def show_strong_more_by_slate_and_risk_type():
    """
    Display STRONG MORE performance grouped by slate date and risk type.

    Lo Note:
    STRONG MORE is the main source of HIGH confidence failure.
    This report checks whether the issue is concentrated on one slate
    or consistent across multiple dates.
    """

    df = pd.read_csv("paper_bets.csv")

    strong_more_df = df[
        (df["recommendation"] == "STRONG MORE") &
        (df["result"] != "PASS")
    ]

    dates = sorted(strong_more_df["game_date"].unique())
    risk_types = sorted(strong_more_df["risk_type"].unique())

    print()
    print("-" * 90)
    print("STRONG MORE BY SLATE AND RISK TYPE")
    print("-" * 90)

    for date in dates:
        print()
        print(date)
        print("-" * 40)

        slate_df = strong_more_df[
            strong_more_df["game_date"] == date
        ]

        for risk_type in risk_types:
            risk_df = slate_df[
                slate_df["risk_type"] == risk_type
            ]

            wins = len(risk_df[risk_df["result"] == "WIN"])
            losses = len(risk_df[risk_df["result"] == "LOSS"])
            pushes = len(risk_df[risk_df["result"] == "PUSH"])

            total_graded = wins + losses + pushes

            if total_graded > 0:
                win_rate = round((wins / total_graded) * 100, 2)
            else:
                win_rate = 0

            print(
                f"{risk_type}: "
                f"{wins}-{losses}-{pushes} | "
                f"Win Rate: {win_rate}%"
            )

def show_june_13_strong_more_losses():
    """
    Display all June 13 STRONG MORE losses.

    Lo Note:
    June 13 STRONG MORE plays went 0-23.
    This diagnostic prints the actual failed plays so we can look for
    player, stat, line, or risk-type patterns before changing scoring logic.
    """

    df = pd.read_csv("paper_bets.csv")

    losses_df = df[
        (df["game_date"] == "2026-06-13") &
        (df["recommendation"] == "STRONG MORE") &
        (df["result"] == "LOSS")
    ]

    print()
    print("-" * 90)
    print("JUNE 13 STRONG MORE LOSSES")
    print("-" * 90)

    if losses_df.empty:
        print("No June 13 STRONG MORE losses found.")
        return

    for _, row in losses_df.iterrows():
        print(
            f"{row['player']} | "
            f"{row['stat']} | "
            f"Line: {row['line']} | "
            f"Actual: {row['actual_stat']} | "
            f"Risk: {row['risk_type']}"
        )

# =============================================================================
# INVESTIGATION REPORT
#
# Purpose:
# Determine whether HIGH confidence failures are concentrated in
# STRONG MORE plays, STRONG LESS plays, or both.
#
# Discovery Trigger:
# HIGH confidence currently performing extremely poorly:
#
# Overall HIGH: 6-32 (15.79%)
# June 13 HIGH: 0-26
#
# Do not modify confidence thresholds until this report is reviewed.
# =============================================================================

#============================================================
# NOTES
#
# Lo Note:
# We are currently loading props from a CSV file.
# This replaces hardcoded test props and moves us one step
# closer to real-world usage.
#
# Future Evolution:
# CSV -> UI Form -> Automated Board Import
#
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
# ============================================================

# ==========================================
# DEV TESTS
# Uncomment when manually testing
# ==========================================

# props_to_compare = load_props_from_csv("props.csv")
# ranked_results = compare_props(props_to_compare)

# show_engine_record()
# show_full_performance_report()
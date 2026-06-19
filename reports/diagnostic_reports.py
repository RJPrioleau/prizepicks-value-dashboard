import pandas as pd


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

def show_confidence_audit():
    """
    Audit HIGH vs MEDIUM confidence performance.

    Why:
    HIGH confidence is underperforming MEDIUM confidence.
    This report helps identify whether the issue is tied to
    recommendation type, sport, or risk type.
    """

    df = pd.read_csv("paper_bets.csv")

    graded_df = df[df["result"].isin(["WIN", "LOSS", "PUSH"])]

    confidence_levels = [
        "HIGH",
        "MEDIUM",
        "LOW"
    ]

    print()
    print("-" * 90)
    print("CONFIDENCE AUDIT")
    print("-" * 90)

    for confidence in confidence_levels:
        confidence_df = graded_df[graded_df["confidence"] == confidence]

        wins = len(confidence_df[confidence_df["result"] == "WIN"])
        losses = len(confidence_df[confidence_df["result"] == "LOSS"])
        pushes = len(confidence_df[confidence_df["result"] == "PUSH"])

        total = wins + losses + pushes

        win_rate = round((wins / total) * 100, 2) if total > 0 else 0

        print()
        print(confidence)
        print(f"Wins: {wins}")
        print(f"Losses: {losses}")
        print(f"Pushes: {pushes}")
        print(f"Win Rate: {win_rate}%")

        if total > 0:
            print()
            print("By Recommendation:")

            recommendation_summary = (
                confidence_df
                .groupby("recommendation")["result"]
                .value_counts()
                .unstack(fill_value=0)
            )

            print(recommendation_summary.to_string())

            print()
            print("By Sport:")

            if "sport" in confidence_df.columns:
                sport_summary = (
                    confidence_df
                    .groupby("sport")["result"]
                    .value_counts()
                    .unstack(fill_value=0)
                )

                print(sport_summary.to_string())
            else:
                print("No sport column found.")

            print()
            print("By Risk Type:")

            risk_summary = (
                confidence_df
                .groupby("risk_type")["result"]
                .value_counts()
                .unstack(fill_value=0)
            )

            print(risk_summary.to_string())

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

def show_ladder_compression_candidates():
    """
    Show ladders where multiple recommended props come from the same
    player/stat/slate/direction.

    Why:
    This helps us see where the engine may be overexposed by saving
    several props from one player read.
    """

    df = pd.read_csv("paper_bets.csv")

    graded_df = df[
        df["recommendation"].isin([
            "STRONG MORE",
            "LEAN MORE",
            "STRONG LESS",
            "LEAN LESS"
        ])
    ].copy()

    if graded_df.empty:
        print("No recommended paper bets found.")
        return

    def get_direction(recommendation):
        if recommendation in ["STRONG MORE", "LEAN MORE"]:
            return "MORE"

        if recommendation in ["STRONG LESS", "LEAN LESS"]:
            return "LESS"

        return "PASS"

    graded_df["direction"] = graded_df["recommendation"].apply(
        get_direction
    )

    graded_df["line"] = pd.to_numeric(
        graded_df["line"],
        errors="coerce"
    )

    if "score" in graded_df.columns:
        graded_df["score"] = pd.to_numeric(
            graded_df["score"],
            errors="coerce"
        )
    else:
        graded_df["score"] = None

    ladder_groups = graded_df.groupby([
        "sport",
        "game_date",
        "player",
        "stat",
        "direction"
    ])

    print()
    print("-" * 90)
    print("LADDER COMPRESSION CANDIDATES")
    print("-" * 90)

    candidate_count = 0

    total_candidate_props = 0
    total_removable_props = 0

    for (sport, game_date, player, stat, direction), group in ladder_groups:
        if len(group) <= 1:
            continue

        candidate_count += 1

        total_candidate_props += len(group)
        total_removable_props += len(group) - 1

        recommendation_rank = {
            "STRONG MORE": 4,
            "STRONG LESS": 4,
            "LEAN MORE": 3,
            "LEAN LESS": 3,
        }

        risk_rank = {
            "GOBLIN": 3,
            "NORMAL": 2,
            "DEMON": 1,
        }

        group["recommendation_rank"] = group["recommendation"].map(
            recommendation_rank
        ).fillna(0)

        group["risk_rank"] = group["risk_type"].map(
            risk_rank
        ).fillna(0)

        group = group.sort_values(
            by=["score", "recommendation_rank", "risk_rank", "line"],
            ascending=[False, False, False, True],
            na_position="last"
        )

        keep_row = group.iloc[0]

        print()
        print(f"{sport} | {game_date} | {player} | {stat} | {direction}")
        print("-" * 90)
        print(f"Prop Count: {len(group)}")
        print(
            f"Suggested Keep: "
            f"{keep_row['line']} | "
            f"{keep_row['risk_type']} | "
            f"{keep_row['recommendation']} | "
            f"Score: {keep_row['score']}"
        )

        print()
        print("Full Ladder:")

        columns = [
            "line",
            "risk_type",
            "recommendation",
            "score",
            "confidence",
            "result",
            "actual_stat"
        ]

        display_df = group[columns].fillna("")
        print(display_df.to_string(index=False))

    print()
    print("-" * 90)
    print("COMPRESSION SUMMARY")
    print("-" * 90)

    print(f"Compression Candidates: {candidate_count}")
    print(f"Props Inside Candidates: {total_candidate_props}")
    print(f"Potential Props Removed: {total_removable_props}")

    if total_candidate_props > 0:
        reduction_pct = round(
            (total_removable_props / total_candidate_props) * 100,
            2
        )

        print(f"Potential Reduction: {reduction_pct}%")

    if candidate_count == 0:
        print("No ladder compression candidates found.")

def show_ladder_compression_simulation():
    """
    Simulate ladder compression.

    Keep only one prop per:

    sport
    slate
    player
    stat
    direction
    risk type

    Goal:
    Determine how historical results change if we reduce
    ladder exposure.
    """

    df = pd.read_csv("paper_bets.csv")

    df = df[
        df["recommendation"].isin([
            "STRONG MORE",
            "LEAN MORE",
            "STRONG LESS",
            "LEAN LESS"
        ])
    ].copy()

    df = df[
        df["result"].isin([
            "WIN",
            "LOSS",
            "PUSH"
        ])
    ].copy()

    def get_direction(recommendation):

        if recommendation in [
            "STRONG MORE",
            "LEAN MORE"
        ]:
            return "MORE"

        if recommendation in [
            "STRONG LESS",
            "LEAN LESS"
        ]:
            return "LESS"

        return "PASS"

    df["direction"] = df["recommendation"].apply(
        get_direction
    )

    recommendation_rank = {
        "STRONG MORE": 4,
        "STRONG LESS": 4,
        "LEAN MORE": 3,
        "LEAN LESS": 3,
    }

    risk_rank = {
        "GOBLIN": 3,
        "NORMAL": 2,
        "DEMON": 1,
    }

    df["recommendation_rank"] = (
        df["recommendation"]
        .map(recommendation_rank)
        .fillna(0)
    )

    df["risk_rank"] = (
        df["risk_type"]
        .map(risk_rank)
        .fillna(0)
    )

    df = df.sort_values(
        by=[
            "recommendation_rank",
            "risk_rank",
            "line"
        ],
        ascending=[
            False,
            False,
            True
        ]
    )

    compressed_df = (
        df
        .groupby([
            "sport",
            "game_date",
            "player",
            "stat",
            "direction",
            "risk_type"
        ])
        .head(1)
        .copy()
    )

    wins = len(
        compressed_df[
            compressed_df["result"] == "WIN"
        ]
    )

    losses = len(
        compressed_df[
            compressed_df["result"] == "LOSS"
        ]
    )

    pushes = len(
        compressed_df[
            compressed_df["result"] == "PUSH"
        ]
    )

    original_wins = len(
        df[df["result"] == "WIN"]
    )

    original_losses = len(
        df[df["result"] == "LOSS"]
    )

    removed_wins = original_wins - wins
    removed_losses = original_losses - losses

    total = wins + losses + pushes

    if total > 0:
        win_rate = round(
            (wins / total) * 100,
            2
        )
    else:
        win_rate = 0

    print()
    print("-" * 90)
    print("LADDER COMPRESSION SIMULATION")
    print("-" * 90)

    print(f"Original Props: {len(df)}")
    print(f"Compressed Props: {len(compressed_df)}")
    print(f"Removed Props: {len(df) - len(compressed_df)}")

    print()

    print(f"Removed Wins: {removed_wins}")
    print(f"Removed Losses: {removed_losses}")

    print()

    print(f"Wins: {wins}")
    print(f"Losses: {losses}")
    print(f"Pushes: {pushes}")
    print(f"Win Rate: {win_rate}%")

def show_ladder_performance():
    """
    Show performance for player/stat ladders.

    A ladder is when the same player has multiple lines for the
    same stat on the same slate.

    Lo Note:
    Goblin and Demon props are MORE-only on PrizePicks.
    This report focuses on grouped player/stat exposure so we can
    separate one bad player read from many duplicated prop losses.
    """

    df = pd.read_csv("paper_bets.csv")

    graded_df = df[
        df["result"].isin(["WIN", "LOSS", "PUSH"])
    ].copy()

    if graded_df.empty:
        print("No graded paper bets found.")
        return

    def get_recommendation_direction(recommendation):
        if recommendation in ["STRONG MORE", "LEAN MORE"]:
            return "MORE"

        if recommendation in ["STRONG LESS", "LEAN LESS"]:
            return "LESS"

        return "PASS"

    graded_df["direction"] = graded_df["recommendation"].apply(
        get_recommendation_direction
    )

    graded_df = graded_df[graded_df["direction"] != "PASS"]


    ladder_groups = (
        graded_df
        .groupby(["sport", "game_date", "player", "stat", "direction"])
    )

    print()
    print("-" * 90)
    print("LADDER PERFORMANCE")
    print("-" * 90)

    ladder_count = 0
    cleared_full_count = 0
    hit_partial_count = 0
    missed_count = 0
    mixed_actuals_count = 0

    total_wins = 0
    total_losses = 0
    total_pushes = 0

    worst_ladders = []

    strong_more_ladders = 0
    lean_more_ladders = 0

    strong_more_misses = 0
    lean_more_misses = 0

    for (sport, game_date, player, stat, direction), group in ladder_groups:
        if len(group) <= 1:
            continue

        ladder_count += 1

        group = group.copy()
        group["line"] = group["line"].astype(float)
        group["actual_stat"] = pd.to_numeric(
            group["actual_stat"],
            errors="coerce"
        )

        actual_values = group["actual_stat"].dropna().unique()

        if len(actual_values) == 1:
            actual_stat = actual_values[0]
        else:
            actual_stat = "MIXED"

        wins = len(group[group["result"] == "WIN"])
        losses = len(group[group["result"] == "LOSS"])
        pushes = len(group[group["result"] == "PUSH"])

        total_wins += wins
        total_losses += losses
        total_pushes += pushes

        lowest_line = group["line"].min()
        highest_line = group["line"].max()

        if actual_stat == "MIXED":
            assessment = "MIXED ACTUALS"
        elif actual_stat > highest_line:
            assessment = "CLEARED FULL LADDER"
        elif actual_stat > lowest_line:
            assessment = "HIT PARTIAL LADDER"
        else:
            assessment = "MISSED LADDER"

        if assessment == "CLEARED FULL LADDER":
            cleared_full_count += 1
        elif assessment == "HIT PARTIAL LADDER":
            hit_partial_count += 1
        elif assessment == "MISSED LADDER":
            missed_count += 1
        else:
            mixed_actuals_count += 1

        if assessment == "MISSED LADDER":

            if "STRONG MORE" in recommendations:
                strong_more_misses += 1

            if "LEAN MORE" in recommendations:
                lean_more_misses += 1

        lines = ", ".join(
            str(line) for line in sorted(group["line"].unique())
        )

        risks = ", ".join(
            sorted(group["risk_type"].dropna().unique())
        )

        recommendations = ", ".join(
            sorted(group["recommendation"].dropna().unique())
        )

        if "STRONG MORE" in recommendations:
            strong_more_ladders += 1

        if "LEAN MORE" in recommendations:
            lean_more_ladders += 1

        print()
        print(f"{sport} | {game_date} | {player} | {stat} | {direction}")
        print("-" * 90)
        print(f"Lines: {lines}")
        print(f"Risks: {risks}")
        print(f"Recommendations: {recommendations}")
        print(f"Actual Stat: {actual_stat}")
        print(f"Ladder Record: {wins}-{losses}-{pushes}")
        print(f"Assessment: {assessment}")

        worst_ladders.append({
            "sport": sport,
            "game_date": game_date,
            "player": player,
            "stat": stat,
            "direction": direction,
            "losses": losses,
            "wins": wins,
            "pushes": pushes,
            "assessment": assessment,
            "lines": lines,
            "risks": risks,
            "recommendations": recommendations
        })

    successful_ladders = cleared_full_count + hit_partial_count

    ladder_success_rate = (
        round((successful_ladders / ladder_count) * 100, 2)
        if ladder_count > 0
        else 0
    )

    total_props = total_wins + total_losses + total_pushes

    prop_win_rate = (
        round((total_wins / total_props) * 100, 2)
        if total_props > 0
        else 0
    )

    print()
    print("-" * 90)
    print("LADDER SUMMARY")
    print("-" * 90)
    print(f"Total Ladders: {ladder_count}")
    print(f"Cleared Full Ladder: {cleared_full_count}")
    print(f"Hit Partial Ladder: {hit_partial_count}")
    print(f"Missed Ladder: {missed_count}")
    print(f"Mixed Actuals: {mixed_actuals_count}")
    print(f"Ladder Success Rate: {ladder_success_rate}%")
    print(f"Prop-Level Record: {total_wins}-{total_losses}-{total_pushes}")
    print(f"Prop Win Rate: {prop_win_rate}%")
    print()
    print("RECOMMENDATION EXPOSURE")
    print("-" * 90)

    print(
        f"STRONG MORE Ladders: "
        f"{strong_more_ladders}"
    )

    print(
        f"STRONG MORE Misses: "
        f"{strong_more_misses}"
    )

    print(
        f"LEAN MORE Ladders: "
        f"{lean_more_ladders}"
    )

    print(
        f"LEAN MORE Misses: "
        f"{lean_more_misses}"
    )

    print()
    print("WORST LADDER EXPOSURE")
    print("-" * 90)

    worst_ladders = sorted(
        worst_ladders,
        key=lambda ladder: ladder["losses"],
        reverse=True
    )

    for ladder in worst_ladders[:10]:
        print(
            f"{ladder['sport']} | "
            f"{ladder['game_date']} | "
            f"{ladder['player']} | "
            f"{ladder['stat']} | "
            f"{ladder['direction']} | "
            f"{ladder['wins']}-{ladder['losses']}-{ladder['pushes']} | "
            f"{ladder['assessment']}"
        )

    if ladder_count == 0:
        print("No ladders found.")

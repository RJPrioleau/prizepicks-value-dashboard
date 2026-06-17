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

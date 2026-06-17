import pandas as pd


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

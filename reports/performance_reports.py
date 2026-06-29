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

def show_engine_record_by_sport():
    """
    Display engine record grouped by sport.

    Why:
    Overall record mixes NBA, WNBA, and future sports together.
    Sport-specific records help us evaluate each engine separately.
    """

    df = pd.read_csv("paper_bets.csv")

    if "sport" not in df.columns:
        df.insert(1, "sport", "UNKNOWN")
        df.to_csv("paper_bets.csv", index=False)

    sports = sorted(df["sport"].dropna().unique())

    print()
    print("-" * 90)
    print("ENGINE RECORD BY SPORT")
    print("-" * 90)

    for sport in sports:
        sport_df = df[df["sport"] == sport]

        wins = len(sport_df[sport_df["result"] == "WIN"])
        losses = len(sport_df[sport_df["result"] == "LOSS"])
        pushes = len(sport_df[sport_df["result"] == "PUSH"])
        pending = len(
            sport_df[
                (sport_df["result"] == "PENDING") &
                (sport_df["recommendation"] != "PASS")
            ]
        )

        total_graded = wins + losses + pushes

        if total_graded > 0:
            win_rate = round((wins / total_graded) * 100, 2)
        else:
            win_rate = 0

        print()
        print(sport)
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

def show_score_performance():
    """
    Display performance grouped by engine score.

    Lo Note:
    Older paper_bets.csv rows may not have score values.
    This report skips blank scores and becomes more useful
    as new boards are saved with score tracking enabled.
    """

    df = pd.read_csv("paper_bets.csv")

    if "score" not in df.columns:
        print()
        print("-" * 90)
        print("SCORE PERFORMANCE")
        print("-" * 90)
        print("No score column found.")
        return

    df["score"] = pd.to_numeric(df["score"], errors="coerce")

    scored_df = df[
        df["score"].notna() &
        df["result"].isin(["WIN", "LOSS", "PUSH"])
    ]

    print()
    print("-" * 90)
    print("SCORE PERFORMANCE")
    print("-" * 90)

    if scored_df.empty:
        print("No graded paper bets with score data yet.")
        return

    for score in sorted(scored_df["score"].unique(), reverse=True):
        score_df = scored_df[scored_df["score"] == score]

        wins = len(score_df[score_df["result"] == "WIN"])
        losses = len(score_df[score_df["result"] == "LOSS"])
        pushes = len(score_df[score_df["result"] == "PUSH"])

        total = wins + losses + pushes
        win_rate = round((wins / total) * 100, 2) if total > 0 else 0

        print()
        print(f"Score: {int(score)}")
        print(f"Total Graded: {total}")
        print(f"Record: {wins}-{losses}-{pushes}")
        print(f"Win Rate: {win_rate}%")

def show_score_performance_by_recommendation():
    """
    Show score performance broken down by recommendation type.
    """

    df = pd.read_csv("paper_bets.csv")

    if "score" not in df.columns:
        print()
        print("-" * 90)
        print("SCORE PERFORMANCE BY RECOMMENDATION")
        print("-" * 90)
        print("No score column found.")
        return

    df["score"] = pd.to_numeric(df["score"], errors="coerce")

    scored_df = df[
        df["score"].notna() &
        df["result"].isin(["WIN", "LOSS", "PUSH"])
    ]

    print()
    print("-" * 90)
    print("SCORE PERFORMANCE BY RECOMMENDATION")
    print("-" * 90)

    if scored_df.empty:
        print("No graded paper bets with score data yet.")
        return

    grouped = scored_df.groupby(
        ["score", "recommendation"]
    )

    for (score, recommendation), group in grouped:

        wins = len(group[group["result"] == "WIN"])
        losses = len(group[group["result"] == "LOSS"])
        pushes = len(group[group["result"] == "PUSH"])

        total = wins + losses + pushes

        win_rate = (
            round((wins / total) * 100, 2)
            if total > 0 else 0
        )

        print()
        print(
            f"Score {int(score)} | "
            f"{recommendation}"
        )
        print(f"Total Graded: {total}")
        print(f"Record: {wins}-{losses}-{pushes}")
        print(f"Win Rate: {win_rate}%")

def show_score_performance_by_risk_type():
    """
    Show score performance broken down by risk_type type.
    """

    df = pd.read_csv("paper_bets.csv")

    if "score" not in df.columns:
        print()
        print("-" * 90)
        print("SCORE PERFORMANCE BY RISK TYPE")
        print("-" * 90)
        print("No score column found.")
        return

    df["score"] = pd.to_numeric(df["score"], errors="coerce")

    scored_df = df[
        df["score"].notna() &
        df["result"].isin(["WIN", "LOSS", "PUSH"])
    ]

    print()
    print("-" * 90)
    print("SCORE PERFORMANCE BY RISK TYPE")
    print("-" * 90)

    if scored_df.empty:
        print("No graded paper bets with score data yet.")
        return

    grouped = scored_df.groupby(
        ["score", "risk_type"]
    )

    for (score, risk_type), group in grouped:

        wins = len(group[group["result"] == "WIN"])
        losses = len(group[group["result"] == "LOSS"])
        pushes = len(group[group["result"] == "PUSH"])

        total = wins + losses + pushes

        win_rate = (
            round((wins / total) * 100, 2)
            if total > 0 else 0
        )

        print()
        print(
            f"Score {int(score)} | "
            f"{risk_type}"
        )
        print(f"Total Graded: {total}")
        print(f"Record: {wins}-{losses}-{pushes}")
        print(f"Win Rate: {win_rate}%")

def show_score_distribution():

    """
    Show how often each score is generated.
    """

    df = pd.read_csv("paper_bets.csv")

    if "score" not in df.columns:
        print()
        print("-" * 90)
        print("SCORE DISTRIBUTION")
        print("-" * 90)
        print("No score column found.")
        return

    df["score"] = pd.to_numeric(df["score"], errors="coerce")

    scored_df = df[df["score"].notna()]

    print()
    print("-" * 90)
    print("SCORE DISTRIBUTION")
    print("-" * 90)

    if scored_df.empty:
        print("No score data found.")
        return

    total = len(scored_df)

    for score in range(5, -6, -1):
        count = len(
            scored_df[
                scored_df["score"] == score
                ]
        )

        percentage = round((count / total) * 100, 2) if total > 0 else 0

        print(
            f"Score {score:>2}: "
            f"{count} ({percentage}%)"
        )

    print()
    print(f"Total Scored Props: {total}")

def show_average_score_analysis():
    """
    Compare average scores for wins and losses.
    """

    df = pd.read_csv("paper_bets.csv")

    if "score" not in df.columns:
        print()
        print("-" * 90)
        print("AVERAGE SCORE ANALYSIS")
        print("-" * 90)
        print("No score column found.")
        return

    df["score"] = pd.to_numeric(df["score"], errors="coerce")

    graded_df = df[
        df["score"].notna() &
        df["result"].isin(["WIN", "LOSS"])
    ]

    winning_scores = graded_df[
        graded_df["result"] == "WIN"
    ]["score"]

    losing_scores = graded_df[
        graded_df["result"] == "LOSS"
    ]["score"]

    average_win_score = round(
        winning_scores.mean(), 2
    )

    average_loss_score = round(
        losing_scores.mean(), 2
    )

    print()
    print("-" * 90)
    print("AVERAGE SCORE ANALYSIS")
    print("-" * 90)

    print(f"Average WIN Score: {average_win_score}")
    print(f"Average LOSS Score: {average_loss_score}")

def show_score_effectiveness():
    df = pd.read_csv("paper_bets.csv")

    df["score"] = pd.to_numeric(
        df["score"],
        errors="coerce"
    )

    scored_df = df[
        df["score"].notna() &
        df["result"].isin(["WIN", "LOSS", "PUSH"])
        ]

    print()
    print("-" * 90)
    print("SCORE EFFECTIVENESS")
    print("-" * 90)

    print(
        f"{'Score':<7}"
        f"{'Total':<8}"
        f"{'Wins':<8}"
        f"{'Losses':<10}"
        f"{'Pushes':<8}"
        f"{'Win Rate'}"
    )

    print("-" * 50)

    for score in sorted(
            scored_df["score"].unique(),
            reverse=True
    ):
        score_df = scored_df[
            scored_df["score"] == score
            ]

        wins = len(
            score_df[
                score_df["result"] == "WIN"
                ]
        )

        losses = len(
            score_df[
                score_df["result"] == "LOSS"
                ]
        )

        pushes = len(
            score_df[
                score_df["result"] == "PUSH"
                ]
        )

        total = wins + losses + pushes

        win_rate = (
            round((wins / total) * 100, 2)
            if total > 0 else 0
        )

        print(
            f"{int(score):<7}"
            f"{total:<8}"
            f"{wins:<8}"
            f"{losses:<10}"
            f"{pushes:<8}"
            f"{win_rate}%"
        )

def show_full_performance_report():
    """
    Display all engine performance reports.
    """
    show_engine_record()
    show_engine_record_by_sport()
    show_recommendation_breakdown()
    show_confidence_breakdown()
    show_risk_breakdown()
    show_score_performance()
    show_score_performance_by_recommendation()
    show_score_performance_by_risk_type()
    show_score_distribution()
    show_average_score_analysis()


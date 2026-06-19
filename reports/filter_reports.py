import pandas as pd


def filter_paper_bets(player=None,sport=None,risk_type=None,slate_date=None,result=None,summary_only=False):
    """
    Filter paper_bets.csv using optional stacked filters.

    Lo Note:
    This is a research tool for quickly finding specific groups of
    saved paper bets without writing one-off pandas commands.
    """

    df = pd.read_csv("paper_bets.csv")

    if player:
        df = df[
            df["player"]
            .str.contains(player, case=False, na=False)
        ]

    if sport:
        df = df[
            df["sport"].str.upper() == sport.upper()
        ]

    if risk_type:
        df = df[
            df["risk_type"].str.upper() == risk_type.upper()
        ]

    if result:
        df = df[
            df["result"].str.upper() == result.upper()
            ]

    if slate_date:
        df = df[
            df["game_date"].astype(str).str.startswith(slate_date)
        ]

    if "score" in df.columns:
        df["score"] = pd.to_numeric(df["score"], errors="coerce")

    df = df.sort_values(
        by=["game_date", "score"],
        ascending=[False, False],
        na_position="last"
    )

    print()
    print("-" * 90)
    print("FILTERED PAPER BETS")
    print("-" * 90)

    if df.empty:
        print("No matching paper bets found.")
        return

    if summary_only:

        wins = len(df[df["result"] == "WIN"])
        losses = len(df[df["result"] == "LOSS"])
        pushes = len(df[df["result"] == "PUSH"])
        pending = len(df[df["result"] == "PENDING"])

        graded = wins + losses + pushes

        if graded > 0:
            win_rate = round((wins / graded) * 100, 2)
        else:
            win_rate = 0

        average_score = ""

        if "score" in df.columns:

            score_series = pd.to_numeric(
                df["score"],
                errors="coerce"
            )

            if score_series.notna().any():
                average_score = round(
                    score_series.mean(),
                    2
                )

        print(f"Matches Found: {len(df)}")
        print()
        print(f"Wins: {wins}")
        print(f"Losses: {losses}")
        print(f"Pushes: {pushes}")
        print(f"Pending: {pending}")
        print(f"Win Rate: {win_rate}%")

        if average_score != "":
            print(f"Average Score: {average_score}")

        return

    columns_to_show = [
        "sport",
        "game_date",
        "player",
        "stat",
        "line",
        "risk_type",
        "recommendation",
        "score",
        "confidence",
        "result",
        "actual_stat",
    ]
    print(f"Matches Found: {len(df)}")
    print()

    display_df = df[columns_to_show].fillna("")
    print(display_df.to_string(index=False))
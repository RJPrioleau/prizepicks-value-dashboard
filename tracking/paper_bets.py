import csv
from datetime import datetime
import pandas as pd


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

    #show_engine_record()
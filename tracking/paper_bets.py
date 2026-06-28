import csv
from datetime import datetime
import pandas as pd

def ensure_paper_bets_schema():
    """
    Ensure paper_bets.csv has the current expected columns.

    Lo Note:
    Older paper_bets.csv files did not include sport.
    This keeps old saved data from crashing newer reports.
    """

    df = pd.read_csv("paper_bets.csv")

    if "sport" not in df.columns:
        df.insert(1, "sport", "UNKNOWN")
        df.to_csv("paper_bets.csv", index=False)

    if "score" not in df.columns:
        confidence_index = df.columns.get_loc("confidence")
        df.insert(confidence_index, "score", "")
        df.to_csv("paper_bets.csv", index=False)

    if "reasons" not in df.columns:
        df["reasons"] = ""
        df.to_csv("paper_bets.csv", index=False)

def determine_result(recommendation, line, actual_stat):
    """
    Determine whether a paper bet won, lost, pushed, or should be ignored.

    Lo Note:
    MORE recommendations win when the actual stat is greater than the line.
    LESS recommendations win when the actual stat is less than the line.
    PASS recommendations are not graded.
    """

    if str(actual_stat).upper() == "DNP":
        return "DNP"

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
    ensure_paper_bets_schema()
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
            prop.get("sport", "UNKNOWN"),
            prop["game_date"],
            prop["player"],
            prop["stat"],
            prop["line"],
            prop["opponent"],
            prop["risk_type"],
            prop["recommendation"],
            prop.get("score", ""),
            prop["confidence"],
            "PENDING",
            "",
            " | ".join(prop.get("reasons", []))
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
    ensure_paper_bets_schema()
    with open("paper_bets.csv", "r", newline="", encoding="utf-8") as file:
        reader = csv.DictReader(file)

        for row in reader:

            if (
                row["game_date"] == prop["game_date"]

                and row.get("sport", "UNKNOWN") == prop.get("sport", "UNKNOWN")
                and row["player"] == prop["player"]
                and row["stat"] == prop["stat"]
                and float(row["line"]) == float(prop["line"])
                and row["risk_type"] == prop["risk_type"]
            ):
                return True

    return False

def update_paper_bet_results():
    ensure_paper_bets_schema()
    df = pd.read_csv("paper_bets.csv")

    game_date_filter = input(
        "Enter game date to update (YYYY-MM-DD), or press Enter to view pending slates: "
    ).strip()



    while True:
        pending_bets = df[
            (df["result"] == "PENDING") &
            (df["recommendation"] != "PASS")
            ].copy()

        if game_date_filter:
            pending_bets = pending_bets[
                pending_bets["game_date"].astype(str) == game_date_filter
                ]
        print()
        print(f"Pending Bets Found: {len(pending_bets)}")

        if pending_bets.empty:
            print("No pending actionable bets to update.")
            break

        print()
        print("PENDING BETS")
        print("-" * 90)

        if not game_date_filter:
            print()
            print("PENDING SLATES")
            print("-" * 90)

            slate_counts = (
                pending_bets
                .groupby("game_date")
                .size()
                .sort_index()
            )

            if slate_counts.empty:
                print("No pending actionable bets found.")
                break

            for game_date, count in slate_counts.items():
                print(f"{game_date}: {count} pending bets")

            print()
            game_date_filter = input(
                "Enter game date to update from above, or press Enter again for all pending: "
            ).strip()

            if game_date_filter:
                pending_bets = pending_bets[
                    pending_bets["game_date"].astype(str) == game_date_filter
                    ]

        grouped = pending_bets.groupby("opponent")

        for opponent, group in grouped:

            print()
            print("-" * 90)
            print(f"OPPONENT: {opponent}")
            print("-" * 90)

            for index, row in group.iterrows():
                print(
                    f"{index}: "
                    f"{row['player']} "
                    f"{row['stat']} "
                    f"{row['line']} "
                    f"{row['recommendation']}"
                )

        selected_index_input = input(
            "Enter index to update (or X to exit): "
        ).strip()

        if selected_index_input.upper() == "X":
            print("Finished updating paper bets.")
            break

        try:
            selected_index = int(selected_index_input)

        except ValueError:
            print("Invalid selection.")
            input("Press Enter to continue...")
            continue

        if selected_index not in df.index:
            print("Invalid selection. That index is not available.")
            input("Press Enter to continue...")
            continue

        if selected_index not in pending_bets.index:
            print("Invalid selection. That index is not in the displayed pending bets.")
            input("Press Enter to continue...")
            continue

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

        actual_stat_input = input("Enter the actual stat, DNP, or X to go back: ").strip()

        if actual_stat_input.upper() == "X":
            print("Cancelled update. Returning to pending bets.")
            input("Press Enter to continue...")
            continue

        if actual_stat_input.upper() == "DNP":
            actual_stat = "DNP"
        else:
            try:
                actual_stat = float(actual_stat_input)
            except ValueError:
                print("Invalid actual stat. Enter a number, DNP, or X.")
                input("Press Enter to continue...")
                continue



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

        update_again = input("Update another bet? Y/N: ").strip().upper()

        if update_again != "Y":
            print("Finished updating paper bets.")
            break

    #show_engine_record()
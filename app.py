import  pandas as pd
import os
from datetime import datetime

def load_props():
    return pd.read_csv("data/props.csv")

def calculate_edges(df):
    df["adjusted_projection"] = (
        df["projection"] + df["matchup_adjustment"]
    )

    df["projection_edge"] = (
        df["adjusted_projection"] - df["pp_line"]
    )
    df["market_edge"] = (
        df["sportsbook_line"] - df["pp_line"]
    )

    df["value_score"] = (
        abs(df["projection_edge"]) * 2
        + abs(df["market_edge"]) * 3
        + (df["last10_hit_rate"]) * 10
    )

    return df

def suggest_pick(row):
    projection_edge = row["projection_edge"]
    market_edge = row["market_edge"]
    hit_rate = row["last10_hit_rate"]
    injury_risk = row["injury_risk"]

    if injury_risk >= 3:
        return "AVOID - injury/news risk"

    if projection_edge >=2 and market_edge >=1 and hit_rate >= 0.60:
        return "STRONG MORE - projection and market support over"

    if projection_edge <= -2 and market_edge <= -1 and hit_rate >= 0.60:
        return "STRONG LESS- projection and market support under"

    if projection_edge >= 1:
        return "LEAN MORE - projection slightly favors over"

    if projection_edge <= -1:
        return "LEAN LESS - projection slightly favors under"

    return "NO PLAY"

def rate_risk(row):
    injury_risk = row["injury_risk"]
    hit_rate = row["last10_hit_rate"]
    matchup_adjustment = row["matchup_adjustment"]

    if injury_risk >= 3:
        return "HIGH RISK - injury/news concern"

    if hit_rate < 0.45:
        return "HIGH RISK - low recent hit rate"

    if matchup_adjustment < -0.75:
        return "MEDIUM RISK - matchup hurts"

    if hit_rate >= 0.60 and injury_risk <= 1:
        return "LOW RISK"

    return "MEDIUM RISK"

def confidence_score(row):
    value_score = row["value_score"]
    risk_rating = row["risk_rating"]

    if value_score >=15 and "LOW RISK" in risk_rating:
        return "HIGH CONFIDENCE"

    if value_score >= 10:
        return "MEDIUM CONFIDENCE"

    return "LOW CONFIDENCE"

def confidence_numeric_score(row):
    confidence = row["confidence"]

    if confidence == "HIGH CONFIDENCE":
        return 3

    if confidence == "MEDIUM CONFIDENCE":
        return 2

    return 1

def classify_play(row):
    confidence = row["confidence"]
    risk_rating = row["risk_rating"]
    value_score = row["value_score"]

    if(
        confidence == "HIGH CONFIDENCE"
        and "LOW RISK" in risk_rating
    ):
        return "SAFE PLAY"

    if value_score >=15:
        return "AGGRESSIVE VALUE PLAY"

    if "HIGH RISK" in risk_rating:
        return "RISKY PLAY"

    return "BALANCED PLAY"

def build_reasoning(row):
    reasons = []

    if row["projection_edge"] >= 2:
        reasons.append("Projection strongly above line")

    elif row["projection_edge"] >= 1:
        reasons.append("Projection slightly above line")

    if row["market_edge"] >= 1:
        reasons.append("Sportsbook market supports value")

    if row["last10_hit_rate"] >= 0.60:
        reasons.append("Strong recent hit rate")

    if row["matchup_adjustment"] > 0:
        reasons.append("Favorable Matchup")

    if row["matchup_adjustment"] < 0:
        reasons.append("Difficult matchup")

    if row["injury_risk"] >= 3:
        reasons.append("Potential injury/news concern")

    return "|".join(reasons)

def save_history(df):
    history = df.copy()

    history["date"] = datetime.now().strftime("%Y-%m-%d")
    history["timestamp"] = datetime.now().strftime("%H:%M:%S")
    history["entry_type"] = "PAPER"

    history["result"] = "PENDING"
    history["actual_stat"] = ""

    history = history[[
        "date",
        "timestamp",
        "entry_type",
        "player",
        "sport",
        "stat",
        "opponent",
        "suggestion",
        "risk_rating",
        "confidence",
        "confidence_numeric",
        "play_type",
        "value_score",
        "result",
        "actual_stat"
    ]]

    existing_history = pd.read_csv("data/history.csv", dtype=str)
    existing_history = existing_history.dropna(how="all")

    if not existing_history.empty:
        existing_history["date"] = pd.to_datetime(
            existing_history["date"], errors="coerce"
        ).dt.strftime("%Y-%m-%d")

        history["date"] = pd.to_datetime(
            history["date"], errors="coerce"
        ).dt.strftime("%Y-%m-%d")

        duplicate_keys = ["date", "player", "stat"]

        history = history.merge(
            existing_history[duplicate_keys],
            on=duplicate_keys,
            how="left",
            indicator=True
        )

        history = history[history["_merge"] == "left_only"]
        history = history.drop(columns=["_merge"])

    if history.empty:
        return

    history.to_csv(
        "data/history.csv",
        mode="a",
        header=False,
        index=False
    )

def show_history_summary():

    history = pd.read_csv("data/history.csv")

    if history.empty:
        print()
        print("No history available yet.")
        return

    total_entries = len(history)

    pending_count = len(
        history[history["result"] == "PENDING"]
    )

    completed_count = len(
        history[history["result"] != "PENDING"]
    )

    win_count = len(
        history[history["result"] == "WIN"]
    )

    loss_count = len(
        history[history["result"] == "LOSS"]
    )

    push_count = len(
        history[history["result"] == "PUSH"]
    )

    graded_count = win_count + loss_count

    if graded_count > 0:
        win_rate = win_count / graded_count
    else:
        win_rate = 0

    print()
    print("=" * 40)
    print("HISTORY SUMMARY")
    print("=" * 40)

    print(f"Total Saved Plays: {total_entries}")
    print(f"Pending Plays: {pending_count}")
    print(f"Completed Plays: {completed_count}")
    print(f"Wins: {win_count}")
    print(f"Losses: {loss_count}")
    print(f"Pushes: {push_count}")
    print(f"Win Rate: {win_rate:.2%}")

    print()
    print("=" * 40)
    print("SPORT BREAKDOWN")
    print("=" * 40)

    sports = history["sport"].unique()

    for sport in sports:

        sport_history = history[
            history["sport"] == sport
            ]

        sport_wins = len(
            sport_history[sport_history["result"] == "WIN"]
        )

        sport_losses = len(
            sport_history[sport_history["result"] == "LOSS"]
        )

        graded = sport_wins + sport_losses

        if graded > 0:
            sport_win_rate = sport_wins / graded
        else:
            sport_win_rate = 0

        print()
        print(f"{sport}")
        print(f"Wins: {sport_wins}")
        print(f"Losses: {sport_losses}")
        print(f"Win Rate: {sport_win_rate:.2%}")

    print()
    print("=" * 40)
    print("CONFIDENCE BREAKDOWN")
    print("=" * 40)

    confidence_levels = history["confidence"].unique()

    for level in confidence_levels:
        confidence_history = history[
            history["confidence"] == level
            ]

        confidence_wins = len(
            confidence_history[
                confidence_history["result"] == "WIN"
                ]
        )

        confidence_losses = len(
            confidence_history[
                confidence_history["result"] == "LOSS"
                ]
        )

        graded = confidence_wins + confidence_losses

        if graded > 0:
            confidence_win_rate = confidence_wins / graded
        else:
            confidence_win_rate = 0

        print()
        print(f"{level}")
        print(f"Wins: {confidence_wins}")
        print(f"Losses: {confidence_losses}")
        print(f"Win Rate: {confidence_win_rate:.2%}")
    print()
    print("=" * 40)
    print("PLAY TYPE BREAKDOWN")
    print("=" * 40)

    play_types = history["play_type"].unique()

    for play_type in play_types:

        play_history = history[
            history["play_type"] == play_type
            ]

        play_wins = len(
            play_history[
                play_history["result"] == "WIN"
                ]
        )

        play_losses = len(
            play_history[
                play_history["result"] == "LOSS"
                ]
        )

        graded = play_wins + play_losses

        if graded > 0:
            play_win_rate = play_wins / graded
        else:
            play_win_rate = 0

        print()
        print(f"{play_type}")
        print(f"Wins: {play_wins}")
        print(f"Losses: {play_losses}")
        print(f"Win Rate: {play_win_rate:.2%}")

    print()
    print("=" * 40)
    print("ENTRY TYPE BREAKDOWN")
    print("=" * 40)

    entry_types = history["entry_type"].unique()

    for entry_type in entry_types:

        entry_history = history[
            history["entry_type"] == entry_type
            ]

        entry_wins = len(
            entry_history[
                entry_history["result"] == "WIN"
                ]
        )

        entry_losses = len(
            entry_history[
                entry_history["result"] == "LOSS"
                ]
        )

        graded = entry_wins + entry_losses

        if graded > 0:
            entry_win_rate = entry_wins / graded
        else:
            entry_win_rate = 0

        print()
        print(f"{entry_type}")
        print(f"Wins: {entry_wins}")
        print(f"Losses: {entry_losses}")
        print(f"Win Rate: {entry_win_rate:.2%}")

    input("\nPress Enter to continue...")

def update_result():
    history = pd.read_csv("data/history.csv", dtype=str)
    history["actual_stat"] = history["actual_stat"].fillna("")

    pending = history[
        history["result"] == "PENDING"
    ]

    if pending.empty:
        print("No pending plays to update.")
        return

    print()
    print("PENDING PLAYS")
    print("=" * 40)

    for index, row in pending.iterrows():
        print(
            f"{index}: {row['player']} - {row['sport']} {row['stat']} vs {row['opponent']}"
        )

    selected_index = int(input("Enter the index to update: "))
    result = input("Enter result (WIN/LOSS/PUSH): ").upper()

    while result not in ["WIN", "LOSS", "PUSH"]:
        print("Invalid result. Please enter WIN, LOSS, or PUSH.")
        result = input("Enter result (WIN/LOSS/PUSH): ").upper()

    actual_stat = input("Enter actual stat: ")

    history.loc[selected_index, "result"] = result
    history.loc[selected_index, "actual_stat"] = actual_stat

    history.to_csv("data/history.csv", index=False)

    print("Result updated.")

    input("\nPress Enter to continue...")

def display_history_rows(rows):

    for _, row in rows.iterrows():

        print()
        print(
            f"{row['date']} {row['timestamp']} | "
            f"{row['player']} | "
            f"{row['sport']} {row['stat']} vs {row['opponent']}"
        )

        print(f"Suggestion: {row['suggestion']}")
        print(f"Play Type: {row['play_type']}")
        print(f"Confidence: {row['confidence']}")
        print(f"Result: {row['result']} | Actual Stat: {row['actual_stat']}")
        print("-" * 60)

def view_history():

    history = pd.read_csv("data/history.csv")

    if history.empty:
        print("No history available.")
        return

    print()
    print("=" * 60)
    print("PLAY HISTORY")
    print("=" * 60)

    display_history_rows(history)

    input("\nPress Enter to continue...")

def view_pending_plays():

    history = pd.read_csv("data/history.csv")

    pending = history[
        history["result"] == "PENDING"
    ]

    if pending.empty:
        print()
        print("No pending plays.")
        return

    print()
    print("=" * 60)
    print("PENDING PLAYS")
    print("=" * 60)

    display_history_rows(pending)

    input("\nPress Enter to continue...")

def view_completed_plays():

    history = pd.read_csv("data/history.csv")

    completed = history[
        history["result"] != "PENDING"
    ]

    if completed.empty:
        print()
        print("No completed plays.")
        return

    print()
    print("=" * 60)
    print("COMPLETED PLAYS")
    print("=" * 60)

    display_history_rows(completed)

    input("\nPress Enter to continue...")

def view_plays_by_type():

    history = pd.read_csv("data/history.csv")

    if history.empty:
        print()
        print("No history available.")
        input("\nPress Enter to continue...")
        return

    print()
    print("PLAY TYPES")
    print("=" * 40)

    play_types = history["play_type"].dropna().unique()

    for index, play_type in enumerate(play_types, start=1):
        print(f"{index}. {play_type}")

    choice = input("Choose a play type: ")

    try:
        selected_index = int(choice) - 1
        selected_type = play_types[selected_index]

    except:
        print("Invalid choice.")
        input("\nPress Enter to continue...")
        return

    filtered = history[
        history["play_type"] == selected_type
    ]

    print()
    print("=" * 60)
    print(f"{selected_type} PLAYS")
    print("=" * 60)

    display_history_rows(filtered)

    input("\nPress Enter to continue...")

def view_plays_by_sport():

    history = pd.read_csv("data/history.csv")

    if history.empty:
        print()
        print("No history available.")
        input("\nPress Enter to continue...")
        return

    print()
    print("SPORTS")
    print("=" * 40)

    sports = history["sport"].dropna().unique()

    for index, sport in enumerate(sports, start=1):
        print(f"{index}. {sport}")

    choice = input("Choose a sport: ")

    try:
        selected_index = int(choice) - 1
        selected_sport = sports[selected_index]

    except:
        print("Invalid choice.")
        input("\nPress Enter to continue...")
        return

    filtered = history[
        history["sport"] == selected_sport
    ]

    print()
    print("=" * 60)
    print(f"{selected_sport} PLAYS")
    print("=" * 60)

    display_history_rows(filtered)

    input("\nPress Enter to continue...")

def view_winning_plays():

    history = pd.read_csv("data/history.csv")

    wins = history[
        history["result"] == "WIN"
    ]

    if wins.empty:
        print()
        print("No winning plays yet.")
        input("\nPress Enter to continue...")
        return

    print()
    print("=" * 60)
    print("WINNING PLAYS")
    print("=" * 60)

    display_history_rows(wins)

    input("\nPress Enter to continue...")

def view_losing_plays():

    history = pd.read_csv("data/history.csv")

    losses = history[
        history["result"] == "LOSS"
    ]

    if losses.empty:
        print()
        print("No losing plays yet.")
        input("\nPress Enter to continue...")
        return

    print()
    print("=" * 60)
    print("LOSING PLAYS")
    print("=" * 60)

    display_history_rows(losses)

    input("\nPress Enter to continue...")

def view_plays_by_confidence():

    history = pd.read_csv("data/history.csv")

    if history.empty:
        print()
        print("No history available.")
        input("\nPress Enter to continue...")
        return

    print()
    print("CONFIDENCE LEVELS")
    print("=" * 40)

    confidence_levels = history["confidence"].dropna().unique()

    for index, level in enumerate(confidence_levels, start=1):
        print(f"{index}. {level}")

    choice = input("Choose a confidence level: ")

    try:
        selected_index = int(choice) - 1
        selected_confidence = confidence_levels[selected_index]

    except:
        print("Invalid choice.")
        input("\nPress Enter to continue...")
        return

    filtered = history[
        history["confidence"] == selected_confidence
    ]

    print()
    print("=" * 60)
    print(f"{selected_confidence} PLAYS")
    print("=" * 60)

    display_history_rows(filtered)

    input("\nPress Enter to continue...")

def search_history_by_player():

    history = pd.read_csv("data/history.csv")

    if history.empty:
        print()
        print("No history available.")
        input("\nPress Enter to continue...")
        return

    player_search = input("Enter player name to search: ").lower()

    results = history[
        history["player"].str.lower().str.contains(player_search, na=False)
    ]

    if results.empty:
        print()
        print("No matching player found.")
        input("\nPress Enter to continue...")
        return

    print()
    print("=" * 60)
    print("PLAYER SEARCH RESULTS")
    print("=" * 60)

    display_history_rows(results)

    input("\nPress Enter to continue...")

def search_history_by_opponent():

    history = pd.read_csv("data/history.csv")

    if history.empty:
        print()
        print("No history available.")
        input("\nPress Enter to continue...")
        return

    opponent_search = input("Enter opponent to search: ").upper()

    results = history[
        history["opponent"].str.upper().str.contains(opponent_search, na=False)
    ]

    if results.empty:
        print()
        print("No matching opponent found.")
        input("\nPress Enter to continue...")
        return

    print()
    print("=" * 60)
    print("OPPONENT SEARCH RESULTS")
    print("=" * 60)

    display_history_rows(results)

    input("\nPress Enter to continue...")

def search_history_by_stat():

    history = pd.read_csv("data/history.csv")

    if history.empty:
        print()
        print("No history available.")
        input("\nPress Enter to continue...")
        return

    stat_search = input("Enter stat type to search: ").lower()

    results = history[
        history["stat"].str.lower().str.contains(stat_search, na=False)
    ]

    if results.empty:
        print()
        print("No matching stat type found.")
        input("\nPress Enter to continue...")
        return

    print()
    print("=" * 60)
    print("STAT SEARCH RESULTS")
    print("=" * 60)

    display_history_rows(results)

    input("\nPress Enter to continue...")

def search_history_by_result():

    history = pd.read_csv("data/history.csv")

    if history.empty:
        print()
        print("No history available.")
        input("\nPress Enter to continue...")
        return

    result_search = input(
        "Enter result (WIN/LOSS/PUSH/PENDING): "
    ).upper()

    valid_results = ["WIN", "LOSS", "PUSH", "PENDING"]

    if result_search not in valid_results:
        print()
        print("Invalid result type.")
        input("\nPress Enter to continue...")
        return

    results = history[
        history["result"] == result_search
    ]

    if results.empty:
        print()
        print("No matching results found.")
        input("\nPress Enter to continue...")
        return

    print()
    print("=" * 60)
    print(f"{result_search} SEARCH RESULTS")
    print("=" * 60)

    display_history_rows(results)

    input("\nPress Enter to continue...")

def search_history_by_entry_type():

    history = pd.read_csv("data/history.csv")

    if history.empty:
        print()
        print("No history available.")
        input("\nPress Enter to continue...")
        return

    entry_search = input(
        "Enter entry type (PAPER/REAL): "
    ).upper()

    valid_entry_types = ["PAPER", "REAL"]

    if entry_search not in valid_entry_types:
        print()
        print("Invalid entry type.")
        input("\nPress Enter to continue...")
        return

    results = history[
        history["entry_type"] == entry_search
    ]

    if results.empty:
        print()
        print("No matching entry types found.")
        input("\nPress Enter to continue...")
        return

    print()
    print("=" * 60)
    print(f"{entry_search} ENTRY RESULTS")
    print("=" * 60)

    display_history_rows(results)

    input("\nPress Enter to continue...")

def filter_by_sport_and_result():

    history = pd.read_csv("data/history.csv")

    if history.empty:
        print()
        print("No history available.")
        input("\nPress Enter to continue...")
        return

    sport_search = input("Enter sport: ").upper()
    result_search = input("Enter result (WIN/LOSS/PUSH/PENDING): ").upper()

    valid_results = ["WIN", "LOSS", "PUSH", "PENDING"]

    if result_search not in valid_results:
        print()
        print("Invalid result type.")
        input("\nPress Enter to continue...")
        return

    results = history[
        (history["sport"].str.upper() == sport_search)
        & (history["result"] == result_search)
    ]

    if results.empty:
        print()
        print("No matching plays found.")
        input("\nPress Enter to continue...")
        return

    print()
    print("=" * 60)
    print(f"{sport_search} {result_search} PLAYS")
    print("=" * 60)

    display_history_rows(results)

    input("\nPress Enter to continue...")

def view_top_value_plays():
    history = pd.read_csv("data/history.csv")

    top_plays = history.sort_values(by="value_score", ascending=False).head(10)

    if top_plays.empty:
        print()
        print("no history available.")
        input("\nPress Enter to continue...")
        return

    print()
    print("=" * 60)
    print(" TOP Value PLAYS")
    print("=" * 60)

    display_history_rows(top_plays)

    input("\nPress Enter to continue...")

def view_low_value_plays():

    history = pd.read_csv("data/history.csv")

    low_value_plays = history.sort_values(by="value_score", ascending=True).head(10)

    if low_value_plays.empty:
        print()
        print("no history available.")
        input("\nPress Enter to continue...")
        return

    print()
    print("=" * 60)
    print(" LOW VALUE PLAYS")
    print("=" * 60)

    display_history_rows(low_value_plays)

    input("\nPress Enter to continue...")

def view_highest_value_losses():

    history = pd.read_csv("data/history.csv")

    losses = history[
        history["result"] == "LOSS"
    ]

    highest_value_losses = losses.sort_values(
        by="value_score",
        ascending=False
    ).head(10)

    if highest_value_losses.empty:
        print()
        print("No losing plays available.")
        input("\nPress Enter to continue...")
        return

    print()
    print("=" * 60)
    print("HIGHEST VALUE LOSSES")
    print("=" * 60)

    display_history_rows(highest_value_losses)

    input("\nPress Enter to continue...")

def view_highest_value_wins():

    history = pd.read_csv("data/history.csv")


    wins = history[
        history["result"].str.strip().str.upper() == "WIN"
    ]

    highest_value_wins = wins.sort_values(
        by="value_score",
        ascending=False
    ).head(10)

    if highest_value_wins.empty:
        print()
        print("No winning plays available.")
        input("\nPress Enter to continue...")
        return

    print()
    print("=" * 60)
    print("HIGHEST VALUE WINS")
    print("=" * 60)

    display_history_rows(highest_value_wins)

    input("\nPress Enter to continue...")

def view_lowest_value_wins():

    history = pd.read_csv("data/history.csv")


    wins = history[
        history["result"].str.strip().str.upper() == "WIN"
    ]

    lowest_value_wins = wins.sort_values(
        by="value_score",
        ascending=True
    ).head(10)

    if lowest_value_wins.empty:
        print()
        print("No winning plays available.")
        input("\nPress Enter to continue...")
        return

    print()
    print("=" * 60)
    print("LOWEST VALUE WINS")
    print("=" * 60)

    display_history_rows(lowest_value_wins)

    input("\nPress Enter to continue...")

def view_lowest_value_losses():

    history = pd.read_csv("data/history.csv")

    losses = history[
        history["result"] == "LOSS"
    ]

    lowest_value_losses = losses.sort_values(
        by="value_score",
        ascending=True
    ).head(10)

    if lowest_value_losses.empty:
        print()
        print("No losing plays available.")
        input("\nPress Enter to continue...")
        return

    print()
    print("=" * 60)
    print("LOWEST VALUE LOSSES")
    print("=" * 60)

    display_history_rows(lowest_value_losses)

    input("\nPress Enter to continue...")

def view_highest_confidence_plays():

    history = pd.read_csv("data/history.csv")

    top_confidence = history.sort_values(
        by="confidence_numeric",
        ascending=False
    ).head(10)

    if top_confidence.empty:
        print()
        print("No plays available.")
        input("\nPress Enter to continue...")
        return

    print()
    print("=" * 60)
    print("HIGHEST CONFIDENCE PLAYS")
    print("=" * 60)

    display_history_rows(top_confidence)

    input("\nPress Enter to continue...")

def view_lowest_confidence_plays():
    history = pd.read_csv("data/history.csv")

    bottom_confidence = history.sort_values(
        by="confidence_numeric",
        ascending=True
    ).head(10)

    if bottom_confidence.empty:
        print()
        print("No plays available.")
        input("\nPress Enter to continue...")
        return

    print()
    print("=" * 60)
    print("LOWEST CONFIDENCE PLAYS")
    print("=" * 60)

    display_history_rows(bottom_confidence)

    input("\nPress Enter to continue...")

def main():
    props = load_props()

    props = calculate_edges(props)

    props["suggestion"] = props.apply(suggest_pick,axis=1)
    props["risk_rating"] = props.apply(rate_risk, axis=1)
    props["confidence"] = props.apply(confidence_score, axis=1)
    props["confidence_numeric"] = props.apply(confidence_numeric_score, axis=1)
    props["play_type"] = props.apply(classify_play, axis=1)
    props["reasoning"] = props.apply(build_reasoning, axis=1)

    props = props.sort_values(by="value_score", ascending=False)

    props = props[
        ~props["suggestion"].str.contains("NO PLAY")
    ]

    props = props.head(3)


    if props.empty:
        print()
        print("No strong value plays found right now.")
        print("Recommendation: PASS or wait for better lines.")
        return

    save_history(props)

    print()
    print("TOP VALUE PLAYS")
    print("=" * 40)
    print()

    for _, row in props.iterrows():
        print("=" * 40)

        print(f"{row['player']} - {row['sport']} {row['stat']} vs {row['opponent']}")
        print(f"PrizePicks Line: {row['pp_line']}")
        print(f"Projection: {row['projection']}")
        print(f"Adjusted Projection: {row['adjusted_projection']:.2f}")
        print(f"Matchup Adjustment: {row['matchup_adjustment']:.2f}")
        print(f"Sportsbook Line: {row['sportsbook_line']}")

        print()

        print(f"Projection Edge: {row['projection_edge']:.2f}")
        print(f"Market Edge: {row['market_edge']:.2f}")
        print(f"Value Score: {row['value_score']:.2f}")

        print()
        print(f"Suggestion: {row['suggestion']}")
        print(f"Risk Rating: {row['risk_rating']}")
        print(f"Confidence: {row['confidence']}")
        print(f"Play Type: {row['play_type']}")
        print(f"Reasoning: {row['reasoning']}")

        print("=" * 40)
        print()

        show_history_summary()
    input("\nPress Enter to continue...")

while True:
    os.system("cls")
    print("=" * 60)
    print("PRIZEPICKS VALUE DASHBOARD")
    print("=" * 60)

    print("1. Run analysis")
    print("2. Update result")
    print("3. View history")
    print("4. View pending plays")
    print("5. View completed plays")
    print("6. View summary")
    print("7. View plays by type")
    print("8. View plays by sport")
    print("9. View winning plays")
    print("10. View losing plays")
    print("11. View plays by confidence")
    print("12. Search history by player")
    print("13. Search history by opponent")
    print("14. Search history by stat")
    print("15. Search history by result")
    print("16. Search history by entry type")
    print("17. Filter by sport and result")
    print("18. Filter by Top value plays")
    print("19. Filter by Low value plays")
    print("20. View High Value Losses")
    print("21. View High Value Wins")
    print("22. View Low Value Wins")
    print("23. View Low Value Losses")
    print("24. View Highest Confidence Plays")
    print("25. View lowest Confidence Plays")
    print("26. Exit")

    choice = input("Choose an option: ")

    if choice == "1":
        main()

    elif choice == "2":
        update_result()

    elif choice == "3":
        view_history()

    elif choice == "4":
        view_pending_plays()

    elif choice == "5":
        view_completed_plays()

    elif choice == "6":
        show_history_summary()

    elif choice == "7":
        view_plays_by_type()

    elif choice == "8":
        view_plays_by_sport()

    elif choice == "9":
        view_winning_plays()

    elif choice == "10":
        view_losing_plays()

    elif choice == "11":
        view_plays_by_confidence()

    elif choice == "12":
        search_history_by_player()

    elif choice == "13":
        search_history_by_opponent()

    elif choice == "14":
        search_history_by_stat()

    elif choice == "15":
        search_history_by_result()

    elif choice == "16":
        search_history_by_entry_type()

    elif choice == "17":
        filter_by_sport_and_result()

    elif choice == "18":
        view_top_value_plays()

    elif choice == "19":
        view_low_value_plays()

    elif choice == "20":
        view_highest_value_losses()

    elif choice == "21":
        view_highest_value_wins()

    elif choice == "22":
        view_lowest_value_wins()

    elif choice == "23":
        view_lowest_value_losses()

    elif choice == "24":
        view_highest_confidence_plays()

    elif choice == "25":
        view_lowest_confidence_plays()

    elif choice == "26":
        print("Goodbye.")
        break

    else:
        print("Invalid choice.")

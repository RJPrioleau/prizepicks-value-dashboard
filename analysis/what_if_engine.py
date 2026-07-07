import pandas as pd
from sports.wnba import get_wnba_player_analysis

"""
What-If Engine

Lo Note:
This module allows experimentation with alternate engine
configurations without modifying historical paper bets.

Historical data remains the source of truth.

All simulations are read-only.
"""

"""
Lo Note:

Historical data is immutable.

Simulations may calculate alternate recommendations,
scores, and records, but they never modify paper_bets.csv.

The purpose of this module is experimentation,
not rewriting history.
"""

from analysis.indicator_weights import INDICATOR_WEIGHTS


def run_weight_simulation(custom_weights):
    """
    Display a comparison between the current engine weights
    and a simulated engine configuration.
    """

    # -------------------------------------------------
    # Header
    # -------------------------------------------------

    print()
    print("-" * 90)
    print("WEIGHT SIMULATION")
    print("-" * 90)

    # -------------------------------------------------
    # Current production weights
    # -------------------------------------------------

    print("Current Engine")

    for indicator, weight in INDICATOR_WEIGHTS.items():
        print(f"{indicator:<25}: {weight}")

    # -------------------------------------------------
    # Simulated weights
    # -------------------------------------------------

    print()
    print("Simulation")

    for indicator, weight in custom_weights.items():
        print(f"{indicator:<25}: {weight}")

    # -------------------------------------------------
    # Weight changes
    # -------------------------------------------------

    print()
    print("WEIGHT CHANGES")
    print("-" * 50)

    changes_found = False

    for indicator, current_weight in INDICATOR_WEIGHTS.items():

        new_weight = custom_weights.get(
            indicator,
            current_weight
        )

        if new_weight != current_weight:

            changes_found = True

            change = new_weight - current_weight

            print(
                f"{indicator:<25}"
                f"{current_weight} -> {new_weight}"
                f" ({change:+})"
            )

    if not changes_found:
        print("No weight changes detected.")

    # -------------------------------------------------
    # Replay Engine (Coming Next)
    # -------------------------------------------------

    replay_historical_props(custom_weights)

def replay_historical_props(custom_weights):
    """
    Replay historical props using simulated indicator weights.

    Lo Note:
    This function is the foundation of the What-If Engine.
    It will evaluate hypothetical engine configurations without
    modifying paper_bets.csv.
    """

    print()
    print("-" * 90)
    print("HISTORICAL REPLAY")
    print("-" * 90)

    df = pd.read_csv("paper_bets.csv")

    replay_df = df[
        df["result"].isin(["WIN", "LOSS", "PUSH"]) &
        df["score"].notna()
        ].copy()

    changed_props = []

    print(f"Historical Rows Loaded: {len(df)}")
    print(f"Replay-Eligible Rows: {len(replay_df)}")

    for _, row in replay_df.iterrows():

        replay_result = replay_single_prop(
            row,
            custom_weights
        )

        if replay_result["recommendation"] != row["recommendation"]:
            changed_props.append({
                "player": row["player"],
                "original": row["recommendation"],
                "simulation": replay_result["recommendation"],
                "original_score": row["score"],
                "simulation_score": replay_result["score"],
                "result": row["result"]
            })

    print()
    print(f"Changed Recommendations: {len(changed_props)}")

    changed_wins = len([p for p in changed_props if p["result"] == "WIN"])
    changed_losses = len([p for p in changed_props if p["result"] == "LOSS"])
    changed_pushes = len([p for p in changed_props if p["result"] == "PUSH"])

    print(f"Changed Wins: {changed_wins}")
    print(f"Changed Losses: {changed_losses}")
    print(f"Changed Pushes: {changed_pushes}")

    for prop in changed_props:
        print("-" * 50)
        print(prop["player"])
        print(f"Original: {prop['original']} ({prop['original_score']})")
        print(f"Simulation: {prop['simulation']} ({prop['simulation_score']})")
        print(f"Result: {prop['result']}")

def replay_single_prop(row, custom_weights):
    """
    Replay one historical prop through the correct sport module.

    Lo Note:
    This is the router. It decides which sport-specific
    analysis function should handle the prop.
    """

    sport = row["sport"]

    if sport == "WNBA":
        analysis = get_wnba_player_analysis(
            row["player"],
            row["stat"],
            float(row["line"]),
            row["opponent"],
            indicator_weights=custom_weights
        )
        return analysis

    return {
        "sport": sport,
        "player": row["player"],
        "stat": row["stat"],
        "line": float(row["line"]),
        "status": "ROUTER_READY"
    }
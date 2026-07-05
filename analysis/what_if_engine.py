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

    print(f"Historical Rows Loaded: {len(df)}")
    print(f"Replay-Eligible Rows: {len(replay_df)}")

    sample_row = replay_df.iloc[0]
    replay_result = replay_single_prop(sample_row, custom_weights)
    print()
    print("REPLAY COMPARISON")
    print("-" * 90)

    print(f"Player: {sample_row['player']}")
    print(f"Stat: {sample_row['stat']}")
    print(f"Line: {sample_row['line']}")
    print(f"Opponent: {sample_row['opponent']}")

    print()
    print("Original")
    print("-" * 40)
    print(f"Recommendation: {sample_row['recommendation']}")
    print(f"Score: {sample_row['score']}")

    print()
    print("Simulation")
    print("-" * 40)
    print(f"Recommendation: {replay_result['recommendation']}")
    print(f"Score: {replay_result['score']}")

    score_change = replay_result["score"] - sample_row["score"]

    print()
    print("Difference")
    print("-" * 40)
    print(f"Score Change: {score_change:+}")
    print(
        "Recommendation Changed: "
        f"{replay_result['recommendation'] != sample_row['recommendation']}"
    )

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
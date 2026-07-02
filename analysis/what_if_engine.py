

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

    print("Simulation engine coming soon...")
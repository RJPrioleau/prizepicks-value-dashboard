

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

    print()
    print("-" * 90)
    print("WEIGHT SIMULATION")
    print("-" * 90)

    print("Current Engine")

    for indicator, weight in INDICATOR_WEIGHTS.items():
        print(f"{indicator:<25}: {weight}")

    print()
    print("Simulation")

    for indicator, weight in custom_weights.items():
        print(f"{indicator:<25}: {weight}")

    print()
    print("Simulation engine coming soon...")
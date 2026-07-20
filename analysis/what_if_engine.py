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


def run_weight_simulation(engine_config):
    """
    Display a comparison between the current engine weights
    and a simulated engine configuration.
    """

    simulated_weights = engine_config["indicator_weights"]

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

    for indicator, weight in simulated_weights.items():
        print(f"{indicator:<25}: {weight}")

    # -------------------------------------------------
    # Weight changes
    # -------------------------------------------------

    print()
    print("WEIGHT CHANGES")
    print("-" * 50)

    changes_found = False

    for indicator, current_weight in INDICATOR_WEIGHTS.items():

        new_weight = simulated_weights.get(
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

    replay_historical_props(engine_config)

def  replay_historical_props(engine_config):
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

    strength_only_changes = 0

    print(f"Historical Rows Loaded: {len(df)}")
    print(f"Replay-Eligible Rows: {len(replay_df)}")

    simulation_wins = 0
    simulation_losses = 0
    simulation_pushes = 0
    simulation_ignored = 0

    production_wins = 0
    production_losses = 0
    production_pushes = 0

    for _, row in replay_df.iterrows():

        replay_result = replay_single_prop(
            row,
            engine_config
        )

        simulation_result = score_simulation_result(
            replay_result["recommendation"],
            row["result"]
        )

        if simulation_result == "WIN":
            simulation_wins += 1
        elif simulation_result == "LOSS":
            simulation_losses += 1
        elif simulation_result == "PUSH":
            simulation_pushes += 1
        else:
            simulation_ignored += 1

        if row["result"] == "WIN":
            production_wins += 1
        elif row["result"] == "LOSS":
            production_losses += 1
        elif row["result"] == "PUSH":
            production_pushes += 1

        if replay_result["recommendation"] != row["recommendation"]:

            original = row["recommendation"]
            simulation = replay_result["recommendation"]

            if (
                    (original == "LEAN MORE" and simulation == "STRONG MORE")
                    or (original == "STRONG MORE" and simulation == "LEAN MORE")
                    or (original == "LEAN LESS" and simulation == "STRONG LESS")
                    or (original == "STRONG LESS" and simulation == "LEAN LESS")
            ):
                strength_only_changes += 1

            changed_props.append({
                "player": row["player"],
                "original": original,
                "simulation": simulation,
                "original_score": row["score"],
                "simulation_score": replay_result["score"],
                "result": row["result"]
            })

    production_total = production_wins + production_losses + production_pushes
    simulation_total = simulation_wins + simulation_losses + simulation_pushes

    production_win_rate = (
        round((production_wins / production_total) * 100, 2)
        if production_total > 0 else 0
    )

    simulation_win_rate = (
        round((simulation_wins / simulation_total) * 100, 2)
        if simulation_total > 0 else 0
    )

    print()
    print("PRODUCTION RECORD")
    print("-" * 50)
    print(f"Wins: {production_wins}")
    print(f"Losses: {production_losses}")
    print(f"Pushes: {production_pushes}")

    print(f"Win Rate: {production_win_rate}%")

    print()
    print("SIMULATION RECORD")
    print("-" * 50)
    print(f"Wins: {simulation_wins}")
    print(f"Losses: {simulation_losses}")
    print(f"Pushes: {simulation_pushes}")
    print(f"Ignored: {simulation_ignored}")

    print(f"Win Rate: {simulation_win_rate}%")

    print()
    print("DIFFERENCE")
    print("-" * 50)
    print(f"Win Difference: {simulation_wins - production_wins:+}")
    print(f"Loss Difference: {simulation_losses - production_losses:+}")
    print(f"Win Rate Difference: {round(simulation_win_rate - production_win_rate, 2):+}%")

    print()
    print(f"Changed Recommendations: {len(changed_props)}")
    print(f"Strength Only Changes: {strength_only_changes}")

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

def replay_single_prop(row, engine_config):
    """
    Replay one historical prop through the correct sport module.

    Lo Note:
    This is the router. It decides which sport-specific
    analysis function should handle the prop.
    """

    simulated_weights = engine_config["indicator_weights"]
    simulated_thresholds = engine_config["thresholds"]

    sport = row["sport"]

    if sport == "WNBA":
        analysis = get_wnba_player_analysis(
            row["player"],
            row["stat"],
            float(row["line"]),
            row["opponent"],
            indicator_weights=simulated_weights,
            hit_rate_high_threshold=simulated_thresholds["hit_rate_high"],
            hit_rate_low_threshold=simulated_thresholds["hit_rate_low"],
        )
        return analysis

    return {
        "sport": sport,
        "player": row["player"],
        "stat": row["stat"],
        "line": float(row["line"]),
        "status": "ROUTER_READY"
    }

def score_simulation_result(simulation_recommendation,historical_result):
    """
        Determine the simulated outcome for one historical prop.

        Lo Note:
        If the simulated engine would PASS on the prop,
        it does not receive credit for a win or loss.

        Otherwise, the historical result becomes the
        simulated engine's result.
        """
    """
    Future Enhancement:
    Different recommendation strengths (LEAN vs STRONG)
    currently count equally for simulation records.

    Future engine versions may assign different bet sizes
    or confidence weighting.
    """
    if simulation_recommendation == "PASS":
        return "IGNORE"

    return historical_result
import  pandas as pd

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

def main():
    props = load_props()

    props = calculate_edges(props)

    props["suggestion"] = props.apply(suggest_pick,axis=1)
    props["risk_rating"] = props.apply(rate_risk, axis=1)
    props["confidence"] = props.apply(confidence_score, axis=1)
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


main()

import  pandas as pd

def load_props():
    return pd.read_csv("data/props.csv")

def calculate_edges(df):
    df["projection_edge"] = df["projection"] - df["pp_line"]
    df["market_edge"] = df["sportsbook_line"] - df["pp_line"]

    return df

def suggest_pick(row):
    projection_edge = row["projection_edge"]
    market_edge = row["market_edge"]
    hit_rate = row["last10_hit_rate"]
    injury_risk = row["injury_risk"]

    if injury_risk >= 3:
        return "AVOID - injury/news risk"

    if projection_edge >=2 and market_edge >=1 and hit_rate >= 0.60:
        return "STRONG MORE"

    if projection_edge <= -2 and market_edge <= -1 and hit_rate >= 0.60:
        return "STRONG LESS"

    if projection_edge >= 1:
        return "LEAN MORE"

    if projection_edge <= -1:
        return "LEAN LESS"

    return "NO PLAY"


def main():
    props = load_props()

    props = calculate_edges(props)

    props["suggestion"] = props.apply(suggest_pick,axis=1)


    for _, row in props.iterrows():
        print("=" * 40)

        print(f"{row['player']} - {row['sport']} {row['stat']}")
        print(f"PrizePicks Line: {row['pp_line']}")
        print(f"Projection: {row['projection']}")
        print(f"Sportsbook Line: {row['sportsbook_line']}")

        print()

        print(f"Projection Edge: {row['projection_edge']:.2f}")
        print(f"Market Edge: {row['market_edge']:.2f}")

        print()
        print(f"Suggestion: {row['suggestion']}")

        print("=" * 40)
        print()


main()

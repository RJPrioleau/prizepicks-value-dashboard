import pandas as pd


def load_history(history_file):
    try:
        history_df = pd.read_csv(history_file)
    except FileNotFoundError:
        return pd.DataFrame()

    if history_df.empty:
        return pd.DataFrame()

    return history_df


def calculate_record(history_df):
    completed = history_df[history_df["result"].isin(["WIN", "LOSS", "PUSH"])]

    wins = len(completed[completed["result"] == "WIN"])
    losses = len(completed[completed["result"] == "LOSS"])
    pushes = len(completed[completed["result"] == "PUSH"])

    graded = wins + losses

    win_rate = round((wins / graded) * 100, 2) if graded > 0 else 0

    return wins, losses, pushes, win_rate


def win_rate_by_column(history_df, column_name):

    if column_name not in history_df.columns:
        return pd.DataFrame()

    completed = history_df[history_df["result"].isin(["WIN", "LOSS"])]

    if completed.empty:
        return pd.DataFrame()

    grouped = (
        completed
        .groupby(column_name)["result"]
        .value_counts()
        .unstack(fill_value=0)
    )

    if "WIN" not in grouped.columns:
        grouped["WIN"] = 0

    if "LOSS" not in grouped.columns:
        grouped["LOSS"] = 0

    grouped["total"] = grouped["WIN"] + grouped["LOSS"]

    grouped["win_rate"] = round(
        (grouped["WIN"] / grouped["total"]) * 100,
        2
    )

    return grouped.reset_index()

def get_best_and_worst_segments(history_df, column_name):

    results = win_rate_by_column(history_df, column_name)

    if results.empty:
        return None, None

    best = results.sort_values(by="win_rate", ascending=False).iloc[0]
    worst = results.sort_values(by="win_rate", ascending=True).iloc[0]

    return best, worst

def calculate_projection_accuracy(history_df):
    required_columns = ["projection", "actual_stat"]

    for column in required_columns:
        if column not in history_df.columns:
            return pd.DataFrame()

    completed = history_df[history_df["result"].isin(["WIN", "LOSS", "PUSH"])].copy()

    if completed.empty:
        return pd.DataFrame()

    completed["projection"] = pd.to_numeric(completed["projection"], errors="coerce")
    completed["actual_stat"] = pd.to_numeric(completed["actual_stat"], errors="coerce")

    completed = completed.dropna(subset=["projection", "actual_stat"])

    if completed.empty:
        return pd.DataFrame()

    completed["projection_error"] = completed["actual_stat"] - completed["projection"]
    completed["absolute_error"] = completed["projection_error"].abs()

    return completed
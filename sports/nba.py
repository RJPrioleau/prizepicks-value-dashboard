from nba_api.stats.static import players

def find_player_id(player_name):
    matches = players.find_players_by_full_name(player_name)

    if not matches:
        return None

    return matches[0]["id"]

def add_calculated_stats(df):
    """
    Add PrizePicks-style stat columns that do not exist directly
    in the NBA API game log.

    Lo Note:
    PrizePicks uses stat labels like 3PM and PRA.
    The NBA API may store those stats under different column names
    or require us to calculate them.
    """
    if "FG3M" in df.columns:
        df["3PM"] = df["FG3M"]

    if "FG3A" in df.columns:
        df["3PTA"] = df["FG3A"]

    if "FGM" in df.columns and "FG3M" in df.columns:
        df["2PM"] = df["FGM"] - df["FG3M"]

    if all(column in df.columns for column in ["PTS", "REB", "AST"]):
        df["PRA"] = df["PTS"] + df["REB"] + df["AST"]

    if all(column in df.columns for column in ["REB", "AST"]):
        df["Rebs+Asts"] = df["REB"] + df["AST"]

    return df
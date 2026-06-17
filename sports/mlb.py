

"""
MLB analysis module.

Lo Note:
MLB will require a deeper analysis model than NBA/WNBA.

Basketball props can start with:
- recent averages
- hit rate
- home/away
- opponent average

MLB props will eventually need:
- projected starting pitcher
- batter vs pitcher history
- handedness splits
- pitcher strikeout/contact profile
- lineup spot
- park/weather context
"""

SUPPORTED_MLB_STATS = [
    "Hits",
    "Total Bases",
    "Runs",
    "RBIs",
    "HR",
    "Strikeouts",
    "Pitcher Strikeouts",
]


def get_mlb_player_analysis(player_name, stat_type, line, opponent=None):
    """
    Temporary MLB placeholder.

    This exists so the project has a clear MLB home before we build
    the full baseball engine.
    """

    print("MLB support is not implemented yet.")
    print(f"Requested: {player_name} | {stat_type} {line} vs {opponent}")

    return None
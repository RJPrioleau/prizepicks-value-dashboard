def parse_basketball_matchup(matchup):
    """
    Parse basketball matchup text into location and opponent.

    Supports:
    - "LVA @ DAL"
    - "LVA vs DAL"
    - "LVA vs. DAL"
    """

    if " @ " in matchup:
        parts = matchup.split(" @ ")
        return "Away", parts[1].strip()

    if " vs. " in matchup:
        parts = matchup.split(" vs. ")
        return "Home", parts[1].strip()

    if " vs " in matchup:
        parts = matchup.split(" vs ")
        return "Home", parts[1].strip()

    return None, None
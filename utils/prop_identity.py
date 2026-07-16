

def build_prop_key(prop):
    """
    Build a normalized identity key for a prop.

    This shared key is used anywhere the application needs to compare
    props, detect duplicates, or confirm whether a slate was analyzed.
    """

    return (
        str(prop.get("sport", "UNKNOWN")).strip(),
        str(prop["game_date"]).strip(),
        str(prop["player"]).strip(),
        str(prop["stat"]).strip(),
        str(float(prop["line"])),
        str(prop["risk_type"]).strip(),
    )
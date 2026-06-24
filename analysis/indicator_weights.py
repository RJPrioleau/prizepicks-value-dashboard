

"""
Indicator weights for the recommendation engine.

Lo Note:
These weights let us tune the scoring engine later without
rewriting the recommendation logic.
"""

INDICATOR_WEIGHTS = {
    "last_10_average": 1,
    "season_average": 1,
    "hit_rate": 1,
    "trend": 1,
    "opponent_average": 1,
}
from analysis.indicator_weights import INDICATOR_WEIGHTS

def get_basic_recommendation(line,last_10_avg,season_avg,hit_rate,trend_direction,opponent_avg):
    """
    Generate a recommendation, confidence level, and reasoning.

    Scoring System:
    +1 = Positive indicator
    -1 = Negative indicator

    Indicators:
    - Last 10 average
    - Season average
    - Hit rate
    - Recent trend
    - Opponent history

    Lo Note:
    This is the heart of the recommendation engine.
    Any future improvements to recommendation quality will likely
    happen inside this function.
    """
    score = 0
    reasons = []

    if last_10_avg > line:
        score += INDICATOR_WEIGHTS["last_10_average"]
        reasons.append("Last 10 average is above the line.")
    else:
        score -= INDICATOR_WEIGHTS["last_10_average"]
        reasons.append("Last 10 average is below the line.")

    if season_avg > line:
        score += INDICATOR_WEIGHTS["season_average"]
        reasons.append("Season average is above the line.")
    else:
        score -= INDICATOR_WEIGHTS["season_average"]
        reasons.append("Season average is below the line.")

    if hit_rate >= 60:
        score += INDICATOR_WEIGHTS["hit_rate"]
        reasons.append("Hit rate is 60% or higher.")
    elif hit_rate <= 50:
        score -= INDICATOR_WEIGHTS["hit_rate"]
        reasons.append("Hit rate is 50% or lower.")

    if trend_direction == "UP":
        score += INDICATOR_WEIGHTS["trend"]
        reasons.append("Recent trend is up.")
    elif trend_direction == "DOWN":
        score -= INDICATOR_WEIGHTS["trend"]
        reasons.append("Recent trend is down.")

    if opponent_avg != "N/A":
        if opponent_avg > line:
            score += INDICATOR_WEIGHTS["opponent_average"]
            reasons.append("Opponent average is above the line.")
        else:
            score -= INDICATOR_WEIGHTS["opponent_average"]
            reasons.append("Opponent average is below the line.")

    if score >= 4:
        recommendation = "STRONG MORE"
    elif score >= 2:
        recommendation = "LEAN MORE"
    elif score <= -4:
        recommendation = "STRONG LESS"
    elif score <= -2:
        recommendation = "LEAN LESS"
    else:
        recommendation = "PASS"

    # INVESTIGATION NOTE:
    # HIGH confidence is currently performing poorly:
    # Overall HIGH: 6-32
    # June 13 HIGH: 0-26
    # Do not adjust thresholds yet.
    # Lo Note:
    # Confidence is currently derived directly from score.
    # It is not an independent metric.
    # Any confidence analytics will mirror score analytics
    # until confidence logic is expanded.

    if abs(score) >= 4:
        confidence = "HIGH"
    elif abs(score) >= 2:
        confidence = "MEDIUM"
    else:
        confidence = "LOW"

    return recommendation, score, confidence,  reasons
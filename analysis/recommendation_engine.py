from analysis.indicator_weights import INDICATOR_WEIGHTS

def get_basic_recommendation(line,last_10_avg,season_avg,hit_rate,trend_direction,opponent_avg,indicator_weights=None,hit_rate_high_threshold=60, hit_rate_low_threshold=50):
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
    indicator_breakdown = {}

    weights = indicator_weights or INDICATOR_WEIGHTS



    if last_10_avg > line:
        score += weights["last_10_average"]
        indicator_breakdown["last_10_average"] = weights["last_10_average"]
        reasons.append("Last 10 average is above the line.")
    else:
        score -= weights["last_10_average"]
        indicator_breakdown["last_10_average"] = -weights["last_10_average"]
        reasons.append("Last 10 average is below the line.")

    if season_avg > line:
        score += weights["season_average"]
        indicator_breakdown["season_average"] = weights["season_average"]
        reasons.append("Season average is above the line.")
    else:
        score -= weights["season_average"]
        indicator_breakdown["season_average"] = -weights["season_average"]
        reasons.append("Season average is below the line.")

    if hit_rate >= hit_rate_high_threshold:
        score += weights["hit_rate"]
        indicator_breakdown["hit_rate"] = weights["hit_rate"]
        reasons.append(
            f"Hit rate is {hit_rate_high_threshold}% or higher."
        )

    elif hit_rate <= hit_rate_low_threshold:
        score -= weights["hit_rate"]
        indicator_breakdown["hit_rate"] = -weights["hit_rate"]
        reasons.append(
            f"Hit rate is {hit_rate_low_threshold}% or lower."
        )

    else:
        indicator_breakdown["hit_rate"] = 0

    if trend_direction == "UP":
        score += weights["trend"]
        indicator_breakdown["trend"] = weights["trend"]
        reasons.append("Recent trend is up.")

    elif trend_direction == "DOWN":
        score -= weights["trend"]
        indicator_breakdown["trend"] = -weights["trend"]
        reasons.append("Recent trend is down.")

    else:
        indicator_breakdown["trend"] = 0

    if opponent_avg != "N/A":
        if opponent_avg > line:
            score += weights["opponent_average"]
            indicator_breakdown["opponent_average"] = weights["opponent_average"]
            reasons.append("Opponent average is above the line.")
        else:
            score -= weights["opponent_average"]
            indicator_breakdown["opponent_average"] = -weights["opponent_average"]
            reasons.append("Opponent average is below the line.")
    else:
        indicator_breakdown["opponent_average"] = 0

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
# PrizePicks Dashboard Notes

## Engine Rules

## Design Decisions

### PASS Recommendations
- PASS recommendations are not graded.
- PASS recommendations are not included in engine accuracy metrics.

### Goblin & Demon Rules
- Goblins can only be played MORE.
- Demons can only be played MORE.
- LESS recommendations for Goblins/Demons are converted to PASS.

### Duplicate Detection
- Duplicate Key:
    - game_date
    - player
    - stat
    - line
    - risk_type

Reason:
Prevent duplicate saves while allowing future games with the same player and line.

## 2026-06-11 First Live Test

Engine Record:
12-10 (54.55%)

### Recommendation Breakdown:

STRONG MORE
6-5
54.55%

LEAN MORE
4-4
50.00%

STRONG LESS
0-1
0.00%

LEAN LESS
2-0
100.00%

### Confidence Breakdown

HIGH
6-6 (50%)

MEDIUM
6-4 (60%)

LOW
0-0

Observations:
- First full end-to-end test completed.
- Result grading worked.
- Engine record tracking worked.
- Multi-update workflow worked.
- Need breakdown by recommendation type.
- Need breakdown by confidence level.
- Need breakdown by risk type.
- STRONG MORE and LEAN MORE performed similarly.
- Recommendation strength may not be separating plays effectively.
- Need confidence-level analysis.
- Need larger sample size before adjusting scoring model.
- HIGH confidence underperformed MEDIUM confidence.
- Confidence scoring may not be calibrated correctly.
- Current confidence is derived directly from score thresholds.
- Future improvement: confidence should incorporate hit rate and data quality.

## Analytics Design

Reports are built as individual functions and combined through:

show_full_performance_report()

Reason:
Allows individual reports to be viewed independently while
also supporting a single consolidated analytics report.

# Confidence Scoring Investigation

**Investigation Date:** 2026-06-14

## Objective

Investigate why HIGH confidence recommendations are significantly underperforming before making any changes to confidence thresholds or recommendation scoring logic.

---

## Finding #1 - Overall Performance

### Overall Record

- Record: **26-39**
- Win Rate: **40.00%**

### Confidence Breakdown

| Confidence | Record | Win Rate |
|------------|--------|----------|
| HIGH       | 6-32   | 15.79%   |
| MEDIUM     | 20-7   | 74.07%   |

### Observation

- HIGH confidence recommendations are performing significantly worse than MEDIUM confidence recommendations.

---

## Finding #2 - Confidence Assignment Logic

Current confidence scoring:

```python
if abs(score) >= 4:
    confidence = "HIGH"
elif abs(score) >= 2:
    confidence = "MEDIUM"
else:
    confidence = "LOW"
```

## Finding #3 - High Confidence Breakdown by Recommendation

### Results

| Recommendation | Record | Win Rate |
|----------------|---------|----------|
| STRONG MORE | 6-28 | 17.65% |
| STRONG LESS | 0-4 | 0.00% |

### Observation

The majority of HIGH confidence failures originate from STRONG MORE recommendations.

### Conclusion

The investigation should focus on STRONG MORE recommendations rather than confidence thresholds.

## Finding #4 - Strong More Performance by Slate

### Results

| Slate Date | Record | Win Rate |
|------------|---------|----------|
| 2026-06-10 | 6-5 | 54.55% |
| 2026-06-13 | 0-23 | 0.00% |

### Observation

STRONG MORE recommendations performed reasonably well on June 10 but completely failed on June 13.

### Conclusion

The issue appears concentrated within the June 13 slate rather than being uniformly distributed across all data.

## Finding #5 - Strong More Performance by Risk Type

### Results

| Risk Type | Record |
|-----------|---------|
| DEMON | 0-7 |
| GOBLIN | 5-18 |
| NORMAL | 1-3 |

### Observation

Poor performance is not isolated to a single risk category.

### Conclusion

The STRONG MORE issue affects all risk levels and is not caused solely by DEMON props.

## Finding #6 - Multiple Line Exposure

Board analysis intentionally records each PrizePicks line as a separate playable prop.

This is expected behavior because Goblin, Normal, and Demon props can create multiple valid lines for the same player/stat combination.

Example:

- Jalen Brunson PRA 44.5
- Jalen Brunson PRA 49.5

These are separate props and should remain separate records.

However, for diagnostics, we may also need a grouped view by player/stat.

Reason:

- One player outcome can affect multiple related lines.
- Line-level tracking shows individual prop performance.
- Player/stat grouping shows whether the engine was wrong about the overall player/stat direction.

Future diagnostic:

Create a report that groups results by:

- game_date
- player
- stat
- recommendation

This would help determine whether failures are caused by individual bad lines or broader player/stat prediction misses.

## Finding #7 - June 13 STRONG MORE Loss Concentration

### Results

The June 13 STRONG MORE losses were concentrated across four player/stat groups:

| Player | Stat | Actual |
|--------|------|--------|
| Jose Alvarado | PRA | 1.0 |
| Stephon Castle | PTS | 6.0 |
| Karl-Anthony Towns | PTS | 2.0 |
| De'Aaron Fox | PTS | 7.0 |

### Observation

Although the report showed 23 STRONG MORE losses, those losses came from only four core player/stat predictions.

Each player/stat prediction had multiple related Goblin, Normal, or Demon lines attached.

### Conclusion

The June 13 collapse was not 23 unrelated bad reads.

It was a small number of failed player/stat predictions multiplied across multiple playable lines.

Future diagnostics should include both:

- line-level performance
- grouped player/stat performance

## Finding #8 - Historical Data Source Investigation

### Discovery

Player analysis currently pulls data using:

```python
season="2024-25"
season_type_all_star="Regular Season"
```

## Finding #9 - Data Source Was a Major Contributor

### Discovery

Player analysis was using:

- 2024-25 season
- Regular Season game logs

while evaluating:

- 2026 NBA Finals props

### Result

Jose Alvarado PRA 7.5 changed from:

- STRONG MORE
- Score: 5
- Confidence: HIGH

to:

- PASS
- Score: -1
- Confidence: LOW

without changing any scoring logic.

### Conclusion

Data source accuracy has a larger impact on recommendation quality than confidence thresholds.

Future investigations should verify data sources before modifying recommendation logic.

## Finding #9 - Data Source Significantly Impacts Recommendations

### Discovery

Player analysis was using:

```python
season="2024-25"
season_type_all_star="Regular Season"
```

while evaluating June 2026 NBA Finals props.

### Investigation Results

#### Jose Alvarado PRA 7.5

Old Data Source:
- STRONG MORE
- Score: 5
- Confidence: HIGH

Corrected Data Source:
- PASS
- Score: -1
- Confidence: LOW

#### Karl-Anthony Towns PTS 16.5

Old Data Source:
- STRONG MORE
- Score: 5
- Confidence: HIGH

Corrected Data Source:
- STRONG LESS
- Score: -5
- Confidence: HIGH

Actual Result:
- 2 Points
- STRONG LESS would have been correct

### Observation

Recommendation outputs changed significantly when switching from historical regular-season data to current playoff data.

### Conclusion

Data source selection has a major impact on recommendation quality.

Future investigations should verify season and game log sources before modifying confidence thresholds or scoring logic.
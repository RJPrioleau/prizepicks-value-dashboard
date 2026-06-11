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
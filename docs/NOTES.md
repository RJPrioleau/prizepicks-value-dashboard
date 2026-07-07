# PrizePicks Dashboard Notes

## Purpose

This file documents findings, investigations, design decisions, lessons learned, and future research related to the PrizePicks Value Dashboard.

---

# Engine Rules
### PASS Recommendations

- PASS recommendations are not graded.
- PASS recommendations are not included in engine accuracy metrics.

### Goblin & Demon Rules

- Goblins can only be played MORE.
- Demons can only be played MORE.
- LESS recommendations for Goblins and Demons are converted to PASS.

### Duplicate Detection

Duplicate Key:

- game_date
- player
- stat
- line
- risk_type

Reason:

Prevent duplicate saves while allowing future games with the same player and line.

---

# Design Decisions
### Recommendation Philosophy

The dashboard is a decision-support tool.

The engine provides recommendations, rankings, confidence levels, and supporting data.

The user always makes the final betting decision.

### Recommendation Transparency

Recommendations should always be explainable.

Outputs should include:

- Recommendation
- Recommendation Score
- Confidence
- Supporting Reasons

### Historical Data Philosophy

Historical results are more valuable than assumptions.

Recommendation logic should be adjusted only after sufficient investigation and supporting data.

---

# Analytics Design

Reports are built as individual functions and combined through:

show_full_performance_report()

Reason:

Allows individual reports to be viewed independently while also supporting a single consolidated analytics report.

Current Reports:

- Engine Record Report
- Recommendation Breakdown
- Confidence Breakdown
- Risk Breakdown
- Full Performance Report
- Slate Breakdown
- Recommendation Breakdown by Slate
- Confidence Breakdown by Slate
- High Confidence Breakdown by Recommendation
- Strong More by Risk Type
- Strong More by Slate and Risk Type

---

# Major Findings Summary

### Finding #1

HIGH confidence recommendations significantly underperformed MEDIUM confidence recommendations.

### Finding #4

June 13 was a major outlier slate.

### Finding #7

Many losses originated from a small number of player/stat predictions.

### Finding #9

Incorrect season and game log data was a major contributor to poor recommendations.

### Finding #10

Raw PrizePicks text import is viable.

### Finding #11

WNBA requires a separate player data source.

---

# Confidence Investigation

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

HIGH confidence recommendations are performing significantly worse than MEDIUM confidence recommendations.

---

## Finding #2 - Confidence Assignment Logic

### Current Confidence Scoring

```python
if abs(score) >= 4:
    confidence = "HIGH"
elif abs(score) >= 2:
    confidence = "MEDIUM"
else:
    confidence = "LOW"
```

### Observation

Confidence is currently derived directly from recommendation score thresholds.

No historical performance data is currently used when assigning confidence.

---

## Finding #3 - High Confidence Breakdown by Recommendation

### Results

| Recommendation | Record | Win Rate |
|----------------|--------|----------|
| STRONG MORE    | 6-28   | 17.65%   |
| STRONG LESS    | 0-4    | 0.00%    |

### Observation

The majority of HIGH confidence failures originate from STRONG MORE recommendations.

### Conclusion

The investigation should focus on STRONG MORE recommendations rather than confidence thresholds.

---

## Finding #4 - Strong More Performance by Slate

### Results

| Slate Date | Record | Win Rate |
|------------|--------|----------|
| 2026-06-10 | 6-5    | 54.55%   |
| 2026-06-13 | 0-23   | 0.00%    |

### Observation

STRONG MORE recommendations performed reasonably well on June 10 but completely failed on June 13.

### Conclusion

The issue appears concentrated within the June 13 slate rather than being uniformly distributed across all data.

---

## Finding #5 - Strong More Performance by Risk Type

### Results

| Risk Type | Record |
|-----------|--------|
| DEMON     | 0-7    |
| GOBLIN    | 5-18   |
| NORMAL    | 1-3    |

### Observation

Poor performance is not isolated to a single risk category.

### Conclusion

The STRONG MORE issue affects all risk levels and is not caused solely by DEMON props.

---

## Finding #6 - Multiple Line Exposure

### Discovery

Board analysis intentionally records each PrizePicks line as a separate playable prop.

This is expected behavior because Goblin, Normal, and Demon props can create multiple valid lines for the same player/stat combination.

### Example

- Jalen Brunson PRA 44.5
- Jalen Brunson PRA 49.5

These are separate props and should remain separate records.

### Observation

One player outcome can affect multiple related lines.

Line-level tracking shows individual prop performance.

Player/stat grouping shows whether the engine was correct about the overall player/stat direction.

### Future Diagnostic

Create a report that groups results by:

- game_date
- player
- stat
- recommendation

### Conclusion

Future diagnostics should include both:

- line-level performance
- grouped player/stat performance

---

## Finding #7 - June 13 STRONG MORE Loss Concentration

### Results

The June 13 STRONG MORE losses were concentrated across four player/stat groups:

| Player             | Stat | Actual |
|--------------------|------|--------|
| Jose Alvarado      | PRA  | 1.0    |
| Stephon Castle     | PTS  | 6.0    |
| Karl-Anthony Towns | PTS  | 2.0    |
| De'Aaron Fox       | PTS  | 7.0    |

### Observation

Although the report showed 23 STRONG MORE losses, those losses came from only four core player/stat predictions.

Each player/stat prediction had multiple related Goblin, Normal, or Demon lines attached.

### Conclusion

The June 13 collapse was not 23 unrelated bad reads.

It was a small number of failed player/stat predictions multiplied across multiple playable lines.

Future diagnostics should include both:

- line-level performance
- grouped player/stat performance

## Finding #8 - Historical Data Source Discovery

### Discovery

Player analysis was pulling data using:

```python
season="2024-25"
season_type_all_star="Regular Season"
```

while evaluating June 2026 NBA Finals props.

### Observation

Historical analysis was using data from a different season and different game type than the props being evaluated.

### Conclusion

Data source validation became the next priority of the investigation.

---

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

---

## Finding #10 - Raw Text Import Is Viable

### Discovery

PrizePicks prop cards can be copied directly from WebCatalog.

### Result

A prototype parser successfully converted copied PrizePicks text into:

- player
- stat
- line
- opponent
- risk_type

and generated a valid props.csv file.

### Impact

This removes the need to manually enter props one-by-one into props.csv.

### Completed Improvements

- Game date assignment
- Automatic prop archiving
- Raw prop slate archiving by date

### Remaining Improvements

- Menu integration
- Import validation
- Automatic slate date detection
- Live prop detection
- Additional parser error handling

### Conclusion

Manual prop entry is no longer required for normal workflow.

---

## Finding #11 - WNBA Requires Separate Player Data Source

### Discovery

A temporary WNBA lookup test was run using the current NBA player lookup function.

Test players:

- A'ja Wilson
- Chelsea Gray
- Paige Bueckers
- Olivia Miles

### Result

All test players returned:

```text
None
```

### Observation

The current NBA player lookup method does not include WNBA players.

### Conclusion

WNBA support cannot be added by simply reusing the current NBA player lookup.

Future WNBA support will require:

- A separate WNBA player lookup method
- A WNBA-compatible game log data source
- Validation that stat columns match the existing NBA analysis engine

### Follow-Up Discovery

SportsDataverse provides WNBA roster data including:

- athlete_id
- full_name
- team_abbreviation
- position_name

Example:

A'ja Wilson -> 3149391

This successfully solves the WNBA player lookup problem.

---

# Future Research

## WNBA Data Source

### Current Status

The current NBA player lookup does not support WNBA players.

### Questions

- What API provides WNBA player data?
- Can WNBA game logs be retrieved programmatically?
- Are WNBA stat fields compatible with the existing NBA analysis engine?
- Can WNBA player IDs be resolved similarly to NBA player IDs?

### Success Criteria

- Retrieve WNBA player IDs
- Retrieve WNBA game logs
- Calculate historical averages
- Reuse the existing recommendation engine with minimal modifications

---

## MLB Data Source

### Current Status

Research not yet started.

MLB remains the next major sport expansion after WNBA support is evaluated.

### Questions

- What is the best MLB data source or API?
- How should pitcher props be analyzed?
- How should hitter props be analyzed?
- Should pitcher and hitter recommendations use separate scoring models?
- Which MLB prop types should be supported first?

### Candidate Props

Pitchers:

- Strikeouts
- Earned Runs
- Hits Allowed
- Walks Allowed
- Pitching Outs

Hitters:

- Hits
- Runs
- RBIs
- Total Bases
- Fantasy Score

### Success Criteria

- Retrieve MLB player data
- Retrieve MLB game logs
- Support both pitcher and hitter analysis
- Produce recommendations using the existing dashboard framework
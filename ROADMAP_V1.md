# PrizePicks Value Dashboard Roadmap

## Project Vision

Build a data-driven prop analysis platform that helps users identify value opportunities, track results, improve decision making, and measure the performance of the recommendation engine over time.

---

## Phase 1 - Core Analysis Engine

- [x] Historical player analysis
- [x] Prop comparison engine
- [x] Recommendation scoring
- [x] Confidence scoring
- [x] CSV prop import
- [x] Risk type support (NORMAL/GOBLIN/DEMON)
- [x] Stat alias support (3PM, 3PTA, 2PM, PRA)
- [x] NBA API caching
- [x] No-data player handling
- [x] Real board stress test
- [x] Paper bet CSV generation
- [x] Duplicate detection

### Remaining
- [ ] Improve recommendation logic
- [ ] Goblin/Demon MORE-only recommendation rules
- [ ] Improve ranking quality
- [ ] Additional tie-breakers
- [ ] Improve error handling
- [ ] Expanded testing

### Lo Notes

- PrizePicks boards may contain multiple Goblin and Demon lines for the same player/stat.
- Goblin and Demon props are MORE-only selections.
- Goblin/Demon props should never generate LESS recommendations.
- LESS-side Goblin/Demon recommendations should be converted to PASS.

---

# Phase 2 - Tracking & Validation

## Goals

- [x] Paper bet storage
- [x] Bulk recommendation saving
- [x] Duplicate detection
- [x] Risk breakdown summary
- [x] Save recommendations to paper_bets.csv

### Results Management
- [x] Result grading logic
- [x] Result updates
- [x] Record actual stats
- [ ] Win/Loss tracking

### Engine Evaluation
- [ ] Confidence calibration
- [x] Engine record tracking
- [ ] Recommendation accuracy reporting
- 
- ### Reporting

- [x] Engine Record Report
- [x] Recommendation Breakdown
- [x] Confidence Breakdown
- [x] Risk Breakdown
- [x] Full Performance Report
- [ ] Menu integration

### Lo Note
PrizePicks boards may contain multiple Goblin and Demon lines for the same player/stat.
Do not assume a simple Goblin → Normal → Demon ladder.

## Key Questions

* Are HIGH confidence plays actually performing better?
* Are STRONG recommendations outperforming LEAN recommendations?
* Are the rankings producing positive results?

---

# Phase 3 - Reporting & User Experience

## Goals

# Phase 3 - Reporting & User Experience

- [ ] Custom report sorting
- [ ] Sort by player
- [ ] Sort by risk type
- [ ] Sort by recommendation
- [ ] Sort by confidence
- [ ] Sort by hit rate
- [ ] Sort by score
- [ ] Filter by risk type
- [ ] Filter by recommendation
- [ ] Filter by confidence
- [ ] Top 5 / Top 10 views
- [ ] Export reports
- [ ] Improved report formatting

* Flask web interface
* User-friendly forms
* Dashboard views
* Search and filtering
* Visual analytics

## Future Improvements

* User accounts
* Individual user statistics
* Shared engine statistics

---

# Phase 4 - Expanded Sports Support

## Features
- [ ] User bet tracking
- [ ] Compare user record vs engine record
- [ ] Track overrides of engine recommendations
- [ ] Measure value added by engine

## Planned Sports

* NBA
* MLB
* NFL
* WNBA
* NCAA (future)

## Notes

MLB is the next planned sport after NBA functionality reaches a stable state.

---

# Phase 5 - Advanced Features

## Planned Features

* Suggested slips
* Bankroll management
* Alert system
* Line movement tracking
* Injury/news integration
* Advanced analytics

---

# Phase 6 - Long-Term Vision

## Possible Future Features

* Automated board ingestion
* Machine learning experimentation
* Discord integration
* Friends & family beta testing
* Subscription model evaluation

---

# Design Principles

* User makes the final betting decision.
* The app provides decision support, not automatic betting.
* Recommendations must be explainable.
* Engine performance must be measurable.
* Improvements should be driven by data, not assumptions.

## Refactor Candidate

Move diagnostic reports into:

diagnostics.py

Current diagnostics:

- Engine Record
- Full Performance Report
- Slate Breakdown
- Recommendation Breakdown by Slate
- Confidence Breakdown by Slate
- High Confidence Breakdown by Recommendation
- Strong More by Risk Type
- Strong More by Slate and Risk Type

## Future Enhancement - NBA Season Configuration

Currently, NBA season and season type are controlled by constants in `historical_stats.py`.

Future improvement:

- Move season settings into a config file
- Allow user to select season and season type from the menu
- Prevent future hardcoded season issues

## Future Enhancement - Archive Played Props

Currently, `props.csv` acts as the active working slate file and gets replaced when new props are entered.

Problem:

- Once `props.csv` is replaced, the original slate inputs are lost.
- This makes it harder to re-run old slates with updated engine logic.
- It limits future backtesting, diagnostics, and model comparison.

Future improvement:

- Keep `props.csv` as the active working slate file.
- After board analysis or after results are entered, save a copy of the slate to an archive folder.
- Use file names based on slate date.

Example structure:

```text
data/
  active/
    props.csv

  archive/
    props_2026-06-10.csv
    props_2026-06-13.csv

  results/
    paper_bets.csv
```

## Future Enhancement - Raw PrizePicks Text Importer

Build a tool that imports props from copied PrizePicks board text.

Workflow:

- Open PrizePicks in WebCatalog
- Highlight multiple prop cards
- Copy text
- Paste text into `raw_props.txt`
- Run importer
- Generate `props.csv`

Target output columns:

```csv
player,stat,line,opponent,game_date,risk_type
```

## Importer Note - Mixed Dates

Current raw prop importer uses one manually entered slate date for all imported props.

Limitation:
PrizePicks may show props for multiple dates on the same board.

Current workflow:
Only copy/import props from one slate date at a time.

Future improvement:
Parse the matchup line to detect day/date automatically.

## Importer Limitation - Live Props

The raw text importer can read copied PrizePicks cards, but live/in-progress props may include extra text such as current score, quarter, clock, or current stat value.

Current workflow:

- Prefer importing pregame props only.
- Avoid mixing live props with pregame props in the same import.
- Copy one slate/date at a time.

Future improvement:

- Detect live-game text.
- Flag or skip live props automatically.
- Parse current score/clock only if needed later.
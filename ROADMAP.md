# PrizePicks Value Dashboard

## Project Vision
Build a data-driven sports prop analysis platform that helps identify value opportunities, evaluate recommendation performance, track historical results, and improve decision making through measurable analytics.

The project is designed as a decision-support tool, not an automated betting system. The user always makes the final decision.

Primary goals:

* Analyze player props using historical performance data.
* Generate explainable recommendations.
* Track recommendation performance over time.
* Validate whether the recommendation engine is improving.
* Support multiple sports and prop types.
* Reduce manual workflow through automation and tooling.


## Design Principles
* User makes the final betting decision.
* The application provides decision support, not automatic betting.
* Recommendations must be explainable.
* Engine performance must be measurable.
* Improvements should be driven by data, not assumptions.
* Historical results are more valuable than opinions.
* Automation should eliminate repetitive tasks, not remove user control.


## Current Development Focus
### Active Investigation

#### Confidence Investigation

Current Status:

* Finding #1 through Finding #10 completed.
* Playoff data source bug discovered and fixed.
* Cache key issue discovered and fixed.
* Historical analysis now uses configurable season and season type settings.
* Confidence thresholds have not been adjusted.
* Investigation remains active.

Key Questions:

* Are HIGH confidence plays truly underperforming?
* Are recommendation scores inflated?
* Are Goblin and Demon props impacting results?
* Are recommendation rankings producing positive outcomes?
* Which recommendation categories are performing best?

Current Philosophy:

Do not modify recommendation logic until investigation data supports the change.


---

## Recently Completed Features
### Analysis Engine

- [x] Historical player analysis 
- [x] Recommendation scoring engine
- [x] Confidence scoring engine
- [x] Risk type support (NORMAL, GOBLIN, DEMON)
- [x] Stat alias support (3PM, 3PTA, 2PM, PRA, etc.)
- [x] NBA API integration
- [x] NBA API caching
- [x] No-data player handling
- [x] Opponent history analysis
- [x] Trend analysis
- [x] Home/Away splits
- [x] Recommendation reasoning output
- [x] Initial WNBA data layer (SportsDataverse)

### Tracking & Validation

- [x] Paper bet storage
- [x] Bulk recommendation saving
- [x] Duplicate detection
- [x] Result grading
- [x] Result updates
- [x] Actual stat tracking
- [x] Engine record tracking
- [x] Paper bet history tracking

### Reporting

- [x] Engine Record Report
- [x] Recommendation Breakdown
- [x] Confidence Breakdown
- [x] Risk Breakdown
- [x] Full Performance Report
- [x] Slate Breakdown
- [x] Recommendation Breakdown by Slate
- [x] Confidence Breakdown by Slate
- [x] High Confidence Breakdown by Recommendation
- [x] Strong More by Risk Type
- [x] Strong More by Slate and Risk Type

### Importing & Workflow

- [x] CSV prop import
- [x] Raw PrizePicks text importer
- [x] Slate archiving
- [x] Game date assignment
- [x] Goblin/Demon detection during import
- [x] Opponent extraction during import
- [x] Automatic props.csv generation
- [x] Duplicate protection workflow
- [x] Raw prop slate archiving by game date

### Infrastructure

- [x] Season configuration support
- [x] Season type configuration support
- [x] Cache key improvements
- [x] Playoff data source fixes
- [x] Historical investigation framework
- [x] Findings documentation process (NOTES.md)
- [x] Shared analysis layer
- [x] Shared recommendation engine

### Multi-Sport Support
- [x] Initial WNBA data integration
- [x] WNBA player lookup
- [x] WNBA game log retrieval
- [x] WNBA historical analysis engine
- [x] Shared basketball matchup parser



---

## Next Development Priorities

### High Priority

- [ ] Continue confidence investigation
- [ ] Build WNBA player lookup
- [ ] Build WNBA historical stats engine
- [ ] Integrate WNBA into recommendation engine
- [ ] Validate WNBA recommendations against live props
- [ ] Improve recommendation logic
- [ ] Improve ranking quality

### Medium Priority
- [ ] Menu cleanup
- [ ] Diagnostics refactor
- [ ] Season configuration menu
- [ ] Improve error handling
- [ ] Import validation

### Low Priority
- [ ] Flask dashboard
- [ ] Search and filtering
- [ ] Export reports
- [ ] Visual analytics

---

## Future Features

### Analysis Improvements
- [ ] Goblin/Demon MORE-only recommendation rules
- [ ] Additional recommendation tie-breakers
- [ ] Confidence calibration
- [ ] Recommendation accuracy reporting

### Import Improvements
- [ ] Import validation
- [ ] Duplicate prop detection during import
- [ ] Automatic slate date detection
- [ ] Live prop detection
- [ ] Improved parser error handling
- [ ] Direct WebCatalog integration research

### Reporting & UX
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

### Multi-Sport Support
- [~] WNBA (NBA engine extension)
- [ ] MLB (Next major sport expansion)
- [ ] NFL
- [ ] NCAA

### Advanced Features
- [ ] Suggested slips
- [ ] Bankroll management
- [ ] Alert system
- [ ] Line movement tracking
- [ ] Injury/news integration
- [ ] User bet tracking
- [ ] Compare user record vs engine record
- [ ] Track overrides of engine recommendations
- [ ] Measure value added by engine

---

## Long-Term Vision
- [ ] Automated board ingestion
- [ ] Machine learning experimentation
- [ ] Discord integration
- [ ] Friends & family beta testing
- [ ] Multi-user support
- [ ] Subscription model evaluation
- [ ] Web application deployment

---

## Technical Notes

### Diagnostics Refactor Candidate
Move diagnostic reports into:

- diagnostics.py

Current diagnostics:

- Engine Record
- Full Performance Report
- Slate Breakdown
- Recommendation Breakdown by Slate
- Confidence Breakdown by Slate
- High Confidence Breakdown by Recommendation
- Strong More by Risk Type
- Strong More by Slate and Risk Type

### Season Configuration
Currently, season and season type are controlled through configuration variables.

Future improvements:

- Allow season selection from the menu.
- Allow season type selection (Regular Season, Playoffs).
- Move configuration into a dedicated settings file.
- Prevent future hardcoded season issues.

### Importer Notes
Current Workflow:

1. Open PrizePicks in WebCatalog.
2. Copy prop cards.
3. Paste into raw_props.txt.
4. Run prop_importer.py.
5. Enter slate date.
6. Generate props.csv.

Current Limitations:

- Only import one slate date at a time.
- Live props are not officially supported.
- Date is manually entered.
- Parser assumes standard PrizePicks card formatting.

Future Improvements:

- Automatic slate date detection.
- Live prop detection.
- Import validation.
- Additional board format support.

### Archive Notes
Current Structure:

prop_backups/
    props_YYYY-MM-DD.csv

Purpose:

- Preserve historical slates.
- Allow future backtesting.
- Allow engine comparison against previous versions.
- Support diagnostics and investigations.

Current Behavior:

- Existing props.csv is archived before being overwritten.
- Archive files are named using the slate date.

### WNBA Data Source

SportsDataverse successfully provides:

- WNBA rosters
- Player IDs
- Player game logs
- Historical statistics

Example:

A'ja Wilson -> 3149391

Current implementation status:

- [x] Research complete
- [x] Roster retrieval
- [x] Player lookup proof of concept
- [x] Game log retrieval proof of concept
- [ ] Integration into analysis engine
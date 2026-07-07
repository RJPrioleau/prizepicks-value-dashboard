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

## Current Priority

- [ ] Finish Engine Toolkit v1.0
- [ ] Freeze Engine Toolkit
- [ ] Begin MLB engine implementation
- [ ] Run WNBA + MLB concurrently
- [ ] Expand What-If Engine using live data from both sports

## Core Engine Architecture

### Guiding Principles

- [ ] Build one recommendation engine that supports multiple sports
- [ ] Generalize features whenever they benefit every sport
- [ ] Specialize only when a sport truly requires unique logic
- [ ] The Core Engine should never need to know what sport it is analyzing
- [ ] Build once. Reuse everywhere.
- [ ] Make all engine changes data-driven

---

## Core Engine

### Shared Components

- [ ] Recommendation Engine
- [ ] Score Calculation
- [ ] Confidence System
- [ ] Indicator Weight System
- [ ] Recommendation Reasons
- [ ] Paper Bet Tracking
- [ ] Result Grading
- [ ] Analytics & Performance Reports
- [ ] Diagnostic Reports
- [ ] Ladder Analysis
- [ ] What-If Simulation Engine
- [ ] AI-Assisted Analysis (Future)

---

## Sport Modules

### NBA

- [ ] Historical Statistics
- [ ] Matchup Calculations
- [ ] Sport-Specific Indicators
- [ ] Sport-Specific Weights

### WNBA

- [ ] Historical Statistics
- [ ] Matchup Calculations
- [ ] Sport-Specific Indicators
- [ ] Sport-Specific Weights

### MLB

- [ ] Historical Statistics
- [ ] Matchup Calculations
- [ ] Pitcher/Batter Analysis
- [ ] Sport-Specific Indicators
- [ ] Sport-Specific Weights

### NFL

- [ ] Historical Statistics
- [ ] Matchup Calculations
- [ ] Sport-Specific Indicators
- [ ] Sport-Specific Weights

---

## Engine Toolkit v1.0

### Research & Simulation

- [ ] Indicator Effectiveness Report
- [ ] Grouped Indicator Effectiveness Report
- [ ] Minimum Viable What-If Replay Engine
- [ ] Weight Simulation
- [ ] Toolkit Documentation

### Engine Toolkit Freeze

- [ ] Freeze Engine Toolkit v1.0
- [ ] No new research tools unless they directly improve recommendations or solve a production problem

---

## Engine Development Cycle

- [ ] Load WNBA slate
- [ ] Load MLB slate
- [ ] Paper trade both sports
- [ ] Update results
- [ ] Run diagnostics
- [ ] Review engine performance
- [ ] Test improvements in What-If Engine
- [ ] Apply validated improvements to production engine
- [ ] Repeat

---

## Engine Improvement Rules

- [ ] Reports create evidence
- [ ] Evidence creates hypotheses
- [ ] Simulations test hypotheses
- [ ] Production engine changes only after simulation validation
- [ ] No intuition-only engine changes


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
- [x] Completed first full WNBA board integration and stress test (100 props)
- [x] WNBA Engine v1 Operational

## Analytics Toolkit

- [x] Ladder Analysis
- [x] Confidence Audit
- [x] Sport Performance Tracking
- [x] Filter Engine
- [x] Summary Mode
- [x] Score Tracking

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
- [x] Add stacked filters for `props.csv` and `paper_bets.csv`
  - [x] Filter by player name
  - [x] Filter by risk type
  - [x] Filter by sport
  - [x] Filter by slate date
  - [x] Allow combined filters
    - [x] Example: WNBA + DEMON + June 2026
    - [x] Example: Caitlin Clark + HIGH confidence + LOSS

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

### Mixed NBA/WNBA Slate Support
Status: COMPLETE

- [x] Added `sport` column to props CSV format
- [x] Added automatic routing to NBA and WNBA analysis engines
- [x] Supports mixed NBA and WNBA props in a single slate
- [x] Added sport display column to comparison reports
- [x] Verified with mixed-sport test slate

### Historical Stats Refactor
- [x] Extracted NBA analysis into `sports/nba.py`
- [x] Added WNBA analysis engine in `sports/wnba.py`
- [x] Moved historical calculations into `analysis/historical_analysis.py`
- [x] Moved matchup parsing into `analysis/matchup_parser.py`
- [x] Moved recommendation logic into `analysis/recommendation_engine.py`
- [x] Moved paper betting system into `tracking/paper_bets.py`
- [x] Moved performance reports into `reports/performance_reports.py`
- [x] Moved diagnostic reports into `reports/diagnostic_reports.py`
- [x] Reduced `historical_stats.py` from an all-in-one file to a workflow/orchestration module

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
### Prop Comparison Report Improvements

- [ ] Redesign summary section for better readability
- [ ] Display total props analyzed
- [ ] Display total recommendations made
- [ ] Display total passes
- [ ] Display participation rate (recommendations ÷ total props)
- [ ] Display recommendation rate as a percentage
- [ ] Display recommendation distribution by confidence level
- [ ] Display recommendation distribution by recommendation type
- [ ] Compare current slate participation rate against historical average
- [ ] Compare current slate recommendation distribution against historical averages
- [ ] Support summary reports by day, week, month, sport, and season
- [ ] Add archive/reset capability for long-term engine tracking
- SUMMARY
--------------------------------------------------
Props Analyzed        : 36
Recommendations Made  : 12
Passed                : 24
Participation Rate    : 33.33%
--------------------------------------------------
STRONG MORE           : 4
LEAN MORE             : 2
LEAN LESS             : 5
STRONG LESS           : 1
--------------------------------------------------
Recommendation Mix
Strong More           : 33.3%
Lean More             : 16.7%
Lean Less             : 41.7%
Strong Less           : 8.3%
--------------------------------------------------

Participation Rate
--------------------------------------------------
Today's Slate         : 33.33%
Last 7 Days           : 42.18%
Season Average        : 45.71%

### Board Reporting and Archive System

- [ ] Distinguish current-board reports from historical performance reports
- [ ] Add Props Analyzed to board summary
- [ ] Add Recommendations Made to board summary
- [ ] Add Passed count to board summary
- [ ] Add Participation Rate to board summary
- [ ] Archive board analysis with timestamp
- [ ] Save archived board reports separately from paper_bets.csv
- [ ] Add archive folder for board snapshots
- [ ] Allow resetting current board counters after archive
- [ ] Add historical board summary by date range
- [ ] Add historical board summary by sport

### Confidence Audit

- [ ] Show all HIGH confidence plays
- [ ] Show HIGH confidence wins
- [ ] Show HIGH confidence losses
- [ ] Compare HIGH vs MEDIUM scoring factors
- [ ] Identify why HIGH confidence underperforms

### Engine Audit

- [ ] Measure results by unique player assessment
- [ ] Measure results by individual prop
- [ ] Detect correlated prop clusters

### Paper Bet Tracking Improvements

- [x] Add VOID result support
    - [x] Add DNP result status
  - DNP
  - Injury
  - Did Not Start
  - Void prop
    - Handle injury scratches
    - Handle illness scratches
    - Exclude VOID plays from win/loss calculations
    - Track VOID counts separately in performance reports
- - [ ] Score Analytics Report
    - Score distribution
    - Win rate by score
    - Score by sport
    - Score by risk type
    - Score by recommendation
- [x] Investigate prop importer skipping props
  - Latest board expected 20 props but imported 15
  - Check unsupported stat types
  - Check malformed raw lines
  - Check duplicate detection
  - Add importer summary showing imported vs skipped lines
  - Add skipped-line report with reason

### Recommendation Engine Investigation

- [ ] Investigate HIGH confidence assignment logic
- [ ] Investigate STRONG MORE scoring logic
- [ ] Compare HIGH vs MEDIUM confidence factors
- [ ] Compare STRONG MORE wins vs losses
- [ ] Determine why LEAN LESS significantly outperforms STRONG MORE
- [ ] Add sport-specific performance reports
- [ ] Add sport filter to engine record
- [ ] Add sport filter to recommendation breakdown
- [ ] Add sport filter to confidence breakdown

### Recommendation Engine Analytics

- [ ] Player-level prediction accuracy
- [ ] Prop-level prediction accuracy
- [ ] Correlated prop cluster detection
- [ ] Ladder analysis
- [ ] Single-player exposure analysis
- [ ] Ladder Compression Engine

### Ladder Analysis Engine

- [x] Detect player/stat ladders
- [x] Measure ladder performance
- [ ] Calculate ladder success rate
- [ ] Measure player assessment accuracy
- [ ] Identify best goblin rung
- [ ] Identify best demon rung
- [ ] Reduce duplicate exposure in recommendations
- [ ] Group Goblin ladders
- [ ] Group Demon ladders
- [ ] Calculate hit probability by rung
- [ ] Identify best-value rung
- [ ] Recommend only the best rung
- [ ] Track player-level prediction accuracy
- [ ] Track ladder-level prediction accuracy
- [ ] Add ladder-aware recommendation handling
  - Group same player/stat/risk ladders
  - Recommend only best Goblin rung
  - Recommend only best Demon rung if worth it
  - Track player/stat ladder success separately from prop-level record
  - Limit exposure when one player read creates many props

### Ladder / Correlation System

- Detect multiple props from same player/stat
- Group them into a ladder
- Identify best value rung
- Track player-level accuracy
- Track prop-level accuracy
- Reduce duplicate recommendations

### Performance Analytics Improvements

- [ ] Overall record
- [ ] Record by sport
    - NBA
    - WNBA
    - MLB
- [ ] Record by slate
- [ ] Record by month
- [ ] Record by season

### Paper Bet Data Improvements

- [x] Add sport column to paper_bets.csv
- [ ] Backfill existing UNKNOWN records
    - NBA historical records
    - WNBA historical records
- [ ] Sport-specific performance reports
- [ ] Sport-specific recommendation breakdowns
- [ ] Sport-specific confidence breakdowns
- [ ] Improve missing player handling
  - Track players not found in historical data
  - Distinguish rookie vs missing player vs API issue
  - Export missing-player report after board analysis
  - Avoid repeated warnings for same player

### Result Update Quality of Life Improvements

- [ ] Group pending props by game

- [ ] Display matchup during result updates
- [ ] Display team abbreviation during result updates
- [ ] Allow updating all props from one game before moving to the next
- [ ] Validate selected bet index before updating
    - Show a clear message if the index does not exist
    - Do not crash or continue with invalid selection
- [x] Add exit/back option during result update flow
    - Allow `q`, `quit`, `exit`, or `back`
    - Useful after accidentally choosing to update another bet
- [ ] Add slate/game validation before saving paper bets
    - Confirm all props belong to the intended slate date
    - Flag games that are not scheduled for the selected date
    - Prevent future-date props from being mixed into tonight’s paper bet results
- [ ] Add a way to remove or void an imported game/slate mistake
    - Remove all pending props by matchup
    - Remove all pending props by game date
    - Remove all pending props by team/opponent pair

### Result Update Quality of Life Improvements

- [ ] Group pending props by game
- [ ] Display matchup during result updates
- [ ] Display team abbreviation during result updates
- [ ] Allow updating all props from one game before moving to the next

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
- [ ] Prompt user for sport during import
- [ ] Pass sport into parse_prop_block()
- [ ] Remove hardcoded "WNBA" value
- [ ] Support NBA, WNBA, MLB, NFL imports

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

### MLB Analysis Requirements

- [ ] Create MLB data source module
- [ ] Player lookup
- [ ] Game log retrieval
- [ ] Starting pitcher detection
- [ ] Batter vs pitcher history
- [ ] Batter handedness splits
- [ ] Pitcher handedness
- [ ] Pitcher strikeout/contact profile
- [ ] Team strikeout/contact tendencies
- [ ] Lineup spot context
- [ ] Park factor context
- [ ] Weather/wind context
- [ ] MLB-specific recommendation logic

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

### Future Refactor - Rename historical_stats.py

`historical_stats.py` has been reduced from a large all-in-one file into a smaller workflow/orchestration module.

Current remaining responsibilities:

- Clean game log display
- Single prop analysis display
- CSV prop loading
- Multi-prop comparison/ranking

Potential future names:

- `prop_analysis.py`
- `analysis_workflow.py`
- `prop_workflow.py`

Do not rename yet. Wait until NBA/WNBA mixed slate support is stable.

### Future Refactor - App Menu System

Current state:
- app.py contains menu logic and orchestration
- file is ~1400 lines

Future goal:
- Extract menu systems into dedicated modules
- Reduce app.py to application entry point

Potential structure:

menus/
├── main_menu.py
├── analysis_menu.py
├── reports_menu.py
└── paper_bets_menu.py

## Sport Engine Validation

### WNBA Validation
- [x] WNBA player lookup integration
- [x] WNBA game log retrieval
- [x] WNBA board analysis support
- [x] PTS support
- [x] REB support
- [x] AST support
- [x] PRA support
- [x] Rebs+Asts (RA) support
- [x] Goblin prop support
- [x] Demon prop support
- [x] Multi-game slate support
- [x] Duplicate recommendation detection
- [x] 100-prop WNBA stress test

Known Issues
- [ ] Investigate Olivia Miles player lookup
- [ ] Investigate Azzi Fudd player lookup
- [ ] Investigate Janelle Salaün player lookup

Future WNBA Support
- [ ] PA (Points + Assists)
- [ ] PR (Points + Rebounds)
- [ ] Fantasy Score
- [ ] 3PT Made
- [ ] Additional PrizePicks stat types as discovered
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
- [x] Engine record tracking
- [ ] Confidence calibration
- [ ] Recommendation accuracy reporting

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

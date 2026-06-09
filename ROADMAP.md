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
- [ ] Improve ranking quality
- [ ] Additional tie-breakers
- [ ] Improve error handling
- [ ] Expanded testing

---

# Phase 2 - Tracking & Validation

# Phase 2 - Tracking & Validation

## Goals

- [x] Paper bet storage
- [x] Bulk recommendation saving
- [x] Duplicate detection

### Results Management
- [ ] Result updates
- [ ] Record actual stats
- [ ] Win/Loss tracking

### Engine Evaluation
- [ ] Engine record tracking
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

# Phase 3 - User Experience

## Goals

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

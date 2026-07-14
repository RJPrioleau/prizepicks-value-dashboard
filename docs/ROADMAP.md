# PrizePicks Value Dashboard

## Project Vision

Build a data-driven sports prop analysis platform that improves decision-making through measurable analytics, historical validation, and explainable recommendations.

The application is designed as a decision-support tool, not an automated betting system. The user always makes the final decision.

### Primary Goals

- Analyze player props using historical performance data.
- Generate explainable recommendations.
- Measure recommendation performance over time.
- Validate engine improvements using historical replay.
- Support multiple sports through a shared engine architecture.
- Reduce repetitive manual work through automation.

---

## Design Principles

- The user always makes the final betting decision.
- Recommendations should always be explainable.
- Engine improvements must be be measurable.
- Data takes priority over intuition.
- Historical validation is required before production changes.
- Build once. Reuse everywhere.
- Automation should reduce repetitive work without removing user control.

---

# 🚧 Current Sprint

## Engine Toolkit v1.0

**Status:** 🟡 Active

### Sprint Goal

Complete the Engine Toolkit and validate engine improvements before freezing Version 1.

### Current Objectives

- [ ] Improve What-If Engine reporting
  - [x] Begin indicator contribution tracking in recommendation engine
- [ ] Continue replay investigation
- [ ] Validate recommendation changes using historical replay
- [ ] Identify changes that improve decision quality
- [ ] Freeze Engine Toolkit v1.0

---

# 📅 Next Sprint

## MLB Engine

**Status:** 🔵 Planned

### Objectives

- [ ] Create MLB data source
- [ ] Build MLB historical statistics module
- [ ] Integrate MLB into the shared recommendation engine
- [ ] Run WNBA and MLB concurrently
- [ ] Expand the What-If Engine to support multiple sports

---

# 🔬 Current Investigation

## Confidence Investigation

**Status:** 🟡 Active

### Objective

Determine why certain recommendation categories outperform others and identify which engine changes genuinely improve prediction quality.

---

### Current Findings

Completed:

- ✅ Findings #1 through #10 documented
- ✅ Playoff data source issue resolved
- ✅ Cache key issue resolved
- ✅ Season configuration implemented
- ✅ Season type configuration implemented

Current Status:

- Confidence thresholds remain unchanged.
- Recommendation engine investigation is still active.
- Historical replay is now the primary validation method.

---

### Active Research Questions

- [ ] Are HIGH confidence recommendations actually underperforming?
- [ ] Are recommendation scores inflated?
- [ ] Are Goblin and Demon props affecting overall performance?
- [ ] Are recommendation rankings producing better outcomes?
- [ ] Which recommendation categories consistently perform the best?
- [ ] Which engine changes improve recommendation quality instead of simply changing recommendation strength?

---

### Investigation Philosophy

Do not modify production recommendation logic until historical evidence supports the change.

Every engine change must be validated through replay before entering production.

---

# 🏗 Core Engine Architecture

## Guiding Principles

These principles guide every engine improvement.

- [ ] Build one recommendation engine that supports multiple sports.
- [ ] Generalize features whenever they benefit every sport.
- [ ] Specialize only when a sport requires unique logic.
- [ ] The Core Engine should never need to know what sport it is analyzing.
- [ ] Build once. Reuse everywhere.
- [ ] Every engine change must be supported by measurable evidence.

---

## Shared Engine Components

These systems are intended to be reusable across every supported sport.

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

# 🏀 Sport Modules

The Core Engine is shared across all sports.

Each sport provides only its own historical data, matchup logic, and sport-specific indicators.

---

## NBA

- [ ] Historical Statistics
- [ ] Matchup Calculations
- [ ] Sport-Specific Indicators
- [ ] Sport-Specific Weights

---

## WNBA

- [ ] Historical Statistics
- [ ] Matchup Calculations
- [ ] Sport-Specific Indicators
- [ ] Sport-Specific Weights

---

## MLB

- [ ] Historical Statistics
- [ ] Matchup Calculations
- [ ] Pitcher vs Batter Analysis
- [ ] Sport-Specific Indicators
- [ ] Sport-Specific Weights

---

## NFL

- [ ] Historical Statistics
- [ ] Matchup Calculations
- [ ] Sport-Specific Indicators
- [ ] Sport-Specific Weights

---

# 🛠 Engine Toolkit v1.0

## Purpose

The Engine Toolkit exists to improve the production recommendation engine through measurable research instead of intuition.

The toolkit is not part of the production engine.

Its purpose is to generate evidence before production changes are made.

---

## Research Tools

- [ ] Indicator Effectiveness Report
- [ ] Grouped Indicator Effectiveness Report
- [ ] Historical Replay Engine
- [ ] Weight Simulation Engine
- [ ] Toolkit Documentation

---

## Engine Toolkit Freeze

Version 1.0 will be frozen after the following criteria have been met.

### Completion Criteria

- [ ] Core research tools completed
- [ ] Historical Replay Engine validated
- [ ] Weight Simulation validated
- [ ] Toolkit documentation completed

After Version 1.0 is frozen, no additional research tools should be added unless they directly improve recommendation quality or solve a production problem.

---

# 🔄 Engine Development Cycle

Every engine improvement should follow the same repeatable workflow.

1. Load the current slate.
2. Analyze player props.
3. Generate recommendations.
4. Paper trade recommendations.
5. Grade completed props.
6. Run performance reports.
7. Identify strengths and weaknesses.
8. Form a hypothesis.
9. Test the hypothesis using the What-If Engine.
10. Validate improvements through historical replay.
11. Apply validated improvements to the production engine.
12. Repeat.

---

# 📏 Engine Improvement Rules

Every engine improvement should follow these principles.

- Reports create evidence.
- Evidence creates hypotheses.
- Simulations test hypotheses.
- Production changes require historical validation.
- Data takes priority over intuition.
- Do not optimize for one slate.
- Avoid overfitting historical data.
- Build the production engine from measurable results.

# ✅ Completed Milestones

The following capabilities have been completed and are part of the production engine.

---

## Analysis Engine

- Historical player analysis
- Recommendation scoring engine
- Confidence scoring engine
- Risk type support (NORMAL, GOBLIN, DEMON)
- Stat alias support (3PM, 3PTA, 2PM, PRA, etc.)
- NBA API integration
- NBA API caching
- No-data player handling
- Opponent history analysis
- Trend analysis
- Home/Away splits
- Recommendation reasoning output
- Initial WNBA data layer
- Full WNBA board integration and stress testing
- WNBA Engine Version 1 operational

---

## Analytics Toolkit

- Ladder Analysis
- Confidence Audit
- Sport Performance Tracking
- Filter Engine
- Summary Mode
- Score Tracking

---

## Tracking & Validation

- Paper bet storage
- Bulk recommendation saving
- Duplicate detection
- Result grading
- Result updates
- Actual stat tracking
- Engine record tracking
- Paper bet history tracking

---

## Reporting

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

## Import & Workflow

- CSV prop import
- Raw PrizePicks text importer
- Slate archiving
- Game date assignment
- Goblin/Demon detection
- Opponent extraction
- Automatic props.csv generation
- Duplicate protection workflow
- Raw slate archiving
- Advanced stacked filtering
    - Player
    - Risk Type
    - Sport
    - Slate Date
    - Combined Filters

---

## Infrastructure

- Season configuration support
- Season type configuration support
- Cache key improvements
- Playoff data source fixes
- Historical investigation framework
- Findings documentation process
- Shared analysis layer
- Shared recommendation engine

---

## Multi-Sport Support

- Initial WNBA integration
- WNBA player lookup
- WNBA game log retrieval
- WNBA historical analysis engine
- Shared basketball matchup parser
- Mixed NBA/WNBA slate support

---

## Historical Analysis Refactor

Completed migration from a monolithic analysis file into a modular architecture.

Current architecture includes modules for:

- `sports/`
- `analysis/`
- `reports/`
- `tracking/`

This refactor established the foundation for future multi-sport expansion.

---

# 📊 Analytics & Reporting Roadmap

## Recommendation Analytics

- [ ] Recommendation performance by score range
- [ ] Recommendation performance by confidence level
- [ ] Recommendation performance by risk type
- [ ] Recommendation performance by sport
- [ ] Recommendation performance by statistic
- [ ] Recommendation performance by player position

---

## Historical Replay Analytics

- [ ] Recommendation change summary
- [ ] Recommendation flip analysis
- [ ] Indicator contribution report
- [ ] Weight comparison report
- [ ] Production vs Simulation comparison
- [ ] Simulation leaderboard

---

## Engine Diagnostics

- [ ] Recommendation consistency report
- [ ] Indicator stability report
- [ ] Confidence distribution analysis
- [ ] Recommendation score distribution
- [ ] False positive analysis
- [ ] False negative analysis

---

# 📥 Import & Workflow Roadmap

## Import Improvements

- [ ] Automatic validation before import
- [ ] Improved duplicate detection
- [ ] Better malformed data handling
- [ ] Import summary report
- [ ] Import error logging

---

## Workflow Improvements

- [ ] One-command daily workflow
- [ ] Improved menu navigation
- [ ] Faster report selection
- [ ] Configuration file support

---

# 🚀 Future Features

## MLB Engine

- Complete historical statistics engine
- Pitcher vs Batter analysis
- MLB recommendation engine
- MLB diagnostics
- MLB reporting

---

## NFL Engine

- Historical statistics
- Matchup analysis
- Recommendation engine
- Reporting
- Diagnostics

---

## AI Assistance

Long-term research only.

Potential future capabilities:

- Recommendation summaries
- Engine tuning suggestions
- Report explanations
- Historical pattern recognition

AI should assist analysis.

AI should never make betting decisions.

---

## User Experience

- Graphical Dashboard
- Improved CLI
- Configuration management
- Saved report presets
- Export reports to CSV
- Export reports to Excel

---

# 🌎 Long-Term Vision

The long-term objective is to build a reusable sports analytics platform rather than an NBA or WNBA application.

The recommendation engine should become sport-agnostic.

Each sport should provide only:

- Historical data
- Matchup logic
- Sport-specific indicators

Everything else should be shared.

The Engine Toolkit will continue serving as the research environment for testing hypotheses before production implementation.

Production improvements should always be supported by measurable historical evidence.

---

# 📚 Technical Notes

## Current Architecture Direction

```
Core Engine
│
├── Recommendation Engine
├── Confidence Engine
├── Indicator Weights
├── Analytics
├── Reports
├── Tracking
└── What-If Engine
        │
        ├── NBA Module
        ├── WNBA Module
        ├── MLB Module
        └── NFL Module
```

---

## Engineering Philosophy

- Build one engine.
- Support many sports.
- Research before production.
- Measure before changing.
- Build reusable systems.
- Let data drive decisions.

---

## Notes

This roadmap is intended to guide development, not document history.

Completed work should remain summarized as milestones.

Future work should remain prioritized.

The roadmap should answer one question immediately:

> **What should we build next?**
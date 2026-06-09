# PrizePicks Value Dashboard

A Python-based sports prop analysis tool designed to help identify potential value opportunities, compare props, track performance, and improve betting decision-making through data-driven analysis.

---

## Project Goals

The goal of this project is to build a decision-support tool that:

* Analyzes player props
* Compares multiple opportunities
* Ranks props by value
* Tracks recommendation performance
* Measures engine accuracy over time

Important:

This tool does not place bets automatically.

The user always makes the final betting decision.

---

## Current Features

### Historical Analysis

* Last 5 game averages
* Last 10 game averages
* Season averages
* Home/Away splits
* Opponent-specific averages
* Hit rate calculations
* Trend analysis

### Recommendation Engine

Generates:

* STRONG MORE
* LEAN MORE
* PASS
* LEAN LESS
* STRONG LESS

Along with:

* Confidence ratings
* Recommendation scores
* Supporting reasons

### Prop Comparison Engine

Compare multiple props at once.

Features include:

* Ranking system
* Hit rate tie-breakers
* More-side opportunities
* Less-side opportunities
* Actionable opportunity details

### Risk Types

Supported risk categories:

* NORMAL
* GOBLIN
* DEMON

---

## CSV Input Format

Example:

```csv
player,stat,line,opponent,risk_type
Jalen Brunson,PTS,25.5,BOS,NORMAL
Anthony Edwards,REB,6.5,DEN,DEMON
Jayson Tatum,AST,5.5,IND,NORMAL
```

---

## Project Structure

```text
historical_stats.py
props.csv
README.md
ROADMAP.md
CHANGELOG.md
```

---

## Future Features

Planned enhancements include:

* Paper bet tracking
* Actual bet tracking
* Engine accuracy tracking
* Confidence calibration
* Flask web interface
* MLB support
* Suggested slips
* Bankroll management
* Line movement tracking

See ROADMAP.md for details.

---

## Development Philosophy

* Recommendations should be explainable.
* Decisions should be supported by data.
* Performance should be measurable.
* Improvements should be based on results, not assumptions.

---

## Author Notes

This project is being built as a learning project while developing Python and software engineering skills.

The focus is on building useful tools, learning best practices, and improving through continuous iteration.

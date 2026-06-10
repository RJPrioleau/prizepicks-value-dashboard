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
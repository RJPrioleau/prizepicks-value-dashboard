from sports.wnba import get_wnba_player_game_logs, get_wnba_player_analysis

analysis = get_wnba_player_analysis(
    "A'ja Wilson",
    "PRA",
    35.5,
    "DAL"
)

print(analysis)

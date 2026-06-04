from nba_api.stats.static import players
from nba_api.stats.endpoints import playergamelog


def find_player_id(player_name):
    matches = players.find_players_by_full_name(player_name)

    if not matches:
        print(f"No player found for {player_name}")
        return None

    player = matches[0]
    return player["id"]


def show_last_10_games(player_name, season="2024-25"):
    player_id = find_player_id(player_name)

    if player_id is None:
        return

    game_log = playergamelog.PlayerGameLog(
        player_id=player_id,
        season=season,
        season_type_all_star="Regular Season"
    )

    df = game_log.get_data_frames()[0]
    print(df.columns.tolist())

    print(f"\nLast 10 games for {player_name}")
    print("=" * 60)

    columns = ["GAME_DATE", "MATCHUP", "MIN", "PTS", "REB", "AST"]
    print(df[columns].head(10).to_string(index=False))

    print("\nAverages:")
    print(f"PTS: {round(df['PTS'].head(10).mean(), 2)}")
    print(f"REB: {round(df['REB'].head(10).mean(), 2)}")
    print(f"AST: {round(df['AST'].head(10).mean(), 2)}")


show_last_10_games("Jalen Brunson")
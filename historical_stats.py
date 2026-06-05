from nba_api.stats.static import players
from nba_api.stats.endpoints import playergamelog


def find_player_id(player_name):
    matches = players.find_players_by_full_name(player_name)

    if not matches:
        return None

    return matches[0]["id"]

def parse_matchup(matchup):
    if "@" in matchup:
        location = "Away"
    elif "vs." in matchup:
        location = "Home"
    else:
        location = "Unknown"

    opponent = matchup.split()[-1]

    return location, opponent

def get_hit_rate(player_name, stat_type, line):
    player_id = find_player_id(player_name)

    if player_id is None:
        print("Player not found.")
        return

    game_log = playergamelog.PlayerGameLog(
        player_id=player_id,
        season="2024-25",
        season_type_all_star="Regular Season"
    )

    df = game_log.get_data_frames()[0]

    last_10 = df.head(10)

    hits = (last_10[stat_type] > line).sum()

    hit_rate = round((hits / len(last_10)) * 100, 2)

    print(f"\n{player_name}")
    print(f"{stat_type} Line: {line}")
    print(f"Hit Rate Over: {hits}/{len(last_10)}")
    print(f"Hit Rate: {hit_rate}%")

def get_recent_averages(player_name, stat_type):
    player_id = find_player_id(player_name)

    if player_id is None:
        print("Player not found.")
        return

    game_log = playergamelog.PlayerGameLog(
        player_id=player_id,
        season="2024-25",
        season_type_all_star="Regular Season"
    )

    df = game_log.get_data_frames()[0]

    last_5_avg = round(df[stat_type].head(5).mean(), 2)
    last_10_avg = round(df[stat_type].head(10).mean(), 2)
    season_avg = round(df[stat_type].mean(), 2)

    print(f"\n{player_name}")
    print(f"{stat_type} Recent Averages")
    print("=" * 40)
    print(f"Last 5 Average: {last_5_avg}")
    print(f"Last 10 Average: {last_10_avg}")
    print(f"Season Average: {season_avg}")

def analyze_player_stat(player_name, stat_type, line):
    player_id = find_player_id(player_name)

    if player_id is None:
        print("Player not found.")
        return

    game_log = playergamelog.PlayerGameLog(
        player_id=player_id,
        season="2024-25",
        season_type_all_star="Regular Season"
    )

    df = game_log.get_data_frames()[0]

    last_5 = df.head(5)
    last_10 = df.head(10)

    last_5_avg = round(last_5[stat_type].mean(), 2)
    last_10_avg = round(last_10[stat_type].mean(), 2)
    season_avg = round(df[stat_type].mean(), 2)

    trend = round(last_5_avg - last_10_avg, 2)

    if trend > 0:
        trend_direction = "UP"
    elif trend < 0:
        trend_direction = "DOWN"
    else:
        trend_direction = "FLAT"

    hits = (last_10[stat_type] > line).sum()
    hit_rate = round((hits / len(last_10)) * 100, 2)

    print(f"\n{player_name}")
    print("=" * 40)
    print(f"Stat: {stat_type}")
    print(f"Line: {line}")
    print()
    print(f"Last 5 Average: {last_5_avg}")
    print(f"Last 10 Average: {last_10_avg}")
    print(f"Season Average: {season_avg}")
    print()
    print(f"Trend: {trend_direction} ({trend})")
    print()
    print(f"Hit Rate Over {line}: {hits}/{len(last_10)}")
    print(f"Hit Rate: {hit_rate}%")

def show_clean_game_log(player_name):
    player_id = find_player_id(player_name)

    if player_id is None:
        print("Player not found.")
        return

    game_log = playergamelog.PlayerGameLog(
        player_id=player_id,
        season="2024-25",
        season_type_all_star="Regular Season"
    )

    df = game_log.get_data_frames()[0]

    parsed_matchups = df["MATCHUP"].apply(parse_matchup)

    df["location"] = parsed_matchups.apply(lambda x: x[0])
    df["opponent"] = parsed_matchups.apply(lambda x: x[1])

    print(df[["GAME_DATE", "MATCHUP", "location", "opponent", "PTS", "REB", "AST"]].head(10).to_string(index=False))

def get_home_away_split(player_name, stat_type):
    player_id = find_player_id(player_name)

    if player_id is None:
        print("Player not found.")
        return

    game_log = playergamelog.PlayerGameLog(
        player_id=player_id,
        season="2024-25",
        season_type_all_star="Regular Season"
    )

    df = game_log.get_data_frames()[0]

    parsed_matchups = df["MATCHUP"].apply(parse_matchup)

    df["location"] = parsed_matchups.apply(lambda x: x[0])
    df["opponent"] = parsed_matchups.apply(lambda x: x[1])

    home_games = df[df["location"] == "Home"]
    away_games = df[df["location"] == "Away"]

    home_avg = round(home_games[stat_type].mean(), 2)
    away_avg = round(away_games[stat_type].mean(), 2)

    print(f"\n{player_name}")
    print("=" * 40)
    print(f"{stat_type} Home/Away Split")
    print()
    print(f"Home Games: {len(home_games)}")
    print(f"Home Average: {home_avg}")
    print()
    print(f"Away Games: {len(away_games)}")
    print(f"Away Average: {away_avg}")

def get_opponent_average(player_name, stat_type, opponent):
    player_id = find_player_id(player_name)

    if player_id is None:
        print("Player not found.")
        return

    game_log = playergamelog.PlayerGameLog(
        player_id=player_id,
        season="2024-25",
        season_type_all_star="Regular Season"
    )

    df = game_log.get_data_frames()[0]

    parsed_matchups = df["MATCHUP"].apply(parse_matchup)

    df["location"] = parsed_matchups.apply(lambda x: x[0])
    df["opponent"] = parsed_matchups.apply(lambda x: x[1])

    opponent_games = df[df["opponent"] == opponent]

    if opponent_games.empty:
        print(f"\nNo games found against {opponent}.")
        return

    opponent_avg = round(opponent_games[stat_type].mean(), 2)

    print(f"\n{player_name}")
    print("=" * 40)
    print(f"{stat_type} vs {opponent}")
    print()
    print(f"Games Found: {len(opponent_games)}")
    print(f"Average: {opponent_avg}")

def analyze_player_stat_full(player_name, stat_type, line, opponent):
    player_id = find_player_id(player_name)

    if player_id is None:
        print("Player not found.")
        return

    game_log = playergamelog.PlayerGameLog(
        player_id=player_id,
        season="2024-25",
        season_type_all_star="Regular Season"
    )

    df = game_log.get_data_frames()[0]

    parsed_matchups = df["MATCHUP"].apply(parse_matchup)

    df["location"] = parsed_matchups.apply(lambda x: x[0])
    df["opponent"] = parsed_matchups.apply(lambda x: x[1])

    last_5 = df.head(5)
    last_10 = df.head(10)

    last_5_avg = round(last_5[stat_type].mean(), 2)
    last_10_avg = round(last_10[stat_type].mean(), 2)
    season_avg = round(df[stat_type].mean(), 2)

    trend = round(last_5_avg - last_10_avg, 2)

    if trend > 0:
        trend_direction = "UP"
    elif trend < 0:
        trend_direction = "DOWN"
    else:
        trend_direction = "FLAT"

    hits = (last_10[stat_type] > line).sum()
    hit_rate = round((hits / len(last_10)) * 100, 2)

    home_avg = round(
        df[df["location"] == "Home"][stat_type].mean(), 2
    )

    away_avg = round(
        df[df["location"] == "Away"][stat_type].mean(), 2
    )

    opponent_games = df[df["opponent"] == opponent]

    if len(opponent_games) > 0:
        opponent_avg = round(
            opponent_games[stat_type].mean(), 2
        )
    else:
        opponent_avg = "N/A"

    print(f"\n{player_name}")
    print("=" * 50)
    print(f"Stat: {stat_type}")
    print(f"Line: {line}")
    print(f"Opponent: {opponent}")
    print()
    print(f"Last 5 Average: {last_5_avg}")
    print(f"Last 10 Average: {last_10_avg}")
    print(f"Season Average: {season_avg}")
    print()
    print(f"Trend: {trend_direction} ({trend})")
    print()
    print(f"Hit Rate Over {line}: {hits}/10")
    print(f"Hit Rate: {hit_rate}%")
    print()
    print(f"Home Average: {home_avg}")
    print(f"Away Average: {away_avg}")
    print()
    print(f"{stat_type} Average vs {opponent}: {opponent_avg}")

#get_hit_rate("Jalen Brunson", "PTS", 25.5)
#get_recent_averages("Jalen Brunson", "PTS")
#analyze_player_stat("Jalen Brunson", "PTS", 25.5)
#show_clean_game_log("Jalen Brunson")
#get_home_away_split("Jalen Brunson", "PTS")
#get_opponent_average("Jalen Brunson", "PTS", "BOS")
analyze_player_stat_full(
    "Jalen Brunson",
    "PTS",
    25.5,
    "BOS"
)


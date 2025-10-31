import os
from pathlib import Path
from yfpy.query import YahooFantasySportsQuery

# define league object
class League:
    def __init__(self, league_id, game_code, game_id):
        self.league_id = league_id
        self.game_code = game_code
        self.game_id = game_id

    def print_details(self):
        print(f"League ID: {self.league_id}")
        print(f"Game Code: {self.game_code}")
        print(f"Game ID: {self.game_id}")


# Get League details from .league.env file or user input
# --------------------------------------------------------------
def get_league_details(league_env=None):
    league_id = None
    game_code = None
    game_id = None
    env_file = Path(league_env)
    if env_file.exists():
        with env_file.open() as f:
            for line in f:
                key, value = line.strip().split("=", 1)
                if key == "LEAGUE_ID":
                    league_id = value
                elif key == "GAME_CODE":
                    game_code = value
                elif key == "GAME_ID":
                    game_id = value
    
    return League(league_id, game_code, game_id)

league_details = get_league_details(league_env="env/.league.env")
league_details.print_details()

# Prompt user for missing details
if league_details.league_id is None:
    league_details.league_id = input("Enter your Yahoo Fantasy League ID: ").strip()
if league_details.game_code is None:
    league_details.game_code = input("Enter the game code (e.g., 'nfl', 'mlb'): ").strip()
if league_details.game_id is None:
    league_details.game_id = int(input("Enter the game ID (e.g., 461 for NFL 2025): ").strip())

# Populate .env file with an initial query
# --------------------------------------------------------------
try:
    # Initialize the query object (handles auth automatically)
    query = YahooFantasySportsQuery(
        league_id=league_details.league_id,
        game_code=league_details.game_code,
        game_id=league_details.game_id,
        env_var_fallback=True,
        env_file_location=Path("./env"),
        save_token_data_to_env_file=True,
    )
    # Acknowledge successful authentication
    print("Successfully authenticated and initialized Yahoo Fantasy Sports Query.")
except Exception as e:
    print(f"Error: {e}")
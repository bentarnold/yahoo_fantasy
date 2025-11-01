import os
from pathlib import Path
from yfpy.query import YahooFantasySportsQuery

'''
A class to hold league details.

Args:
    league_id (str): The ID of the league.
    game_code (str): The game code.
    game_id (str): The game ID.
'''
class League:
    def __init__(self, league_id, game_code, game_id):
        self.league_id = league_id
        self.game_code = game_code
        self.game_id = game_id

    def print_details(self):
        print(f"League ID: {self.league_id}")
        print(f"Game Code: {self.game_code}")
        print(f"Game ID: {self.game_id}")


'''
Load league details from a .env file.

Args:
    league_env (str): Path to the .env file containing league details.
Returns:
    League: An instance of the League class with loaded details.
'''
def _load_league_details_from_env(league_env='env/.league.env'):
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

'''
Authenticate and initialize Yahoo Fantasy Sports Query.

Args:
    league_details (League, optional): An instance of the League class.
        If None, details are loaded from .env file.
'''
def authenticate_and_initialize_yf_query(league_details=None):
    if league_details is None:
        league_details = _load_league_details_from_env()
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
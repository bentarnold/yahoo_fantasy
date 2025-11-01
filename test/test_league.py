import pytest
from unittest.mock import Mock, patch
from pathlib import Path

# Import the module to be tested
from yahoo_fantasy.league import _load_league_details_from_env, authenticate_and_initialize_yf_query

# Tests for _load_league_details_from_env function
# ---------------------------------------------------------

# Test 1: Valid .env file
def test_load_league_details_from_env(tmp_path):
    # Create a temporary .env file
    env_file = tmp_path / ".league.env"
    env_file.write_text("LEAGUE_ID=12345\nGAME_CODE=nfl\nGAME_ID=67890\n")

    league_details = _load_league_details_from_env(league_env=str(env_file))

    assert league_details.league_id == "12345"
    assert league_details.game_code == "nfl"
    assert league_details.game_id == "67890"

# Test 2: Missing .env file
def test_load_league_details_from_env_missing_file():
    league_details = _load_league_details_from_env(league_env="non_existent.env")

    assert league_details.league_id is None
    assert league_details.game_code is None
    assert league_details.game_id is None


# Tests for authenticate_and_initialize_yf_query function
# ---------------------------------------------------------

# Fixture to mock League class
@pytest.fixture
def mock_league():
    league = Mock()
    league.league_id = "123"
    league.game_code = "nfl"
    league.game_id = "449"
    return league

# Test 1: league_details is None → calls _load_league_details_from_env
@patch('yahoo_fantasy.league._load_league_details_from_env')
@patch('yahoo_fantasy.league.YahooFantasySportsQuery')
@patch('builtins.print')
def test_authenticate_with_none_loads_from_env(mock_print, mock_query_class, mock_load_env, mock_league):
    # Setup
    mock_load_env.return_value = mock_league
    mock_query_instance = Mock()
    mock_query_class.return_value = mock_query_instance

    # Call function
    authenticate_and_initialize_yf_query(league_details=None)

    # Assert _load_league_details_from_env was called
    mock_load_env.assert_called_once()

    # Assert YahooFantasySportsQuery was initialized with correct args
    mock_query_class.assert_called_once_with(
        league_id="123",
        game_code="nfl",
        game_id="449",
        env_var_fallback=True,
        env_file_location=Path("./env"),
        save_token_data_to_env_file=True,
    )

    # Assert success message printed
    mock_print.assert_called_with("Successfully authenticated and initialized Yahoo Fantasy Sports Query.")


# Test 2: league_details provided → does NOT call _load_league_details_from_env
@patch('yahoo_fantasy.league._load_league_details_from_env')
@patch('yahoo_fantasy.league.YahooFantasySportsQuery')
@patch('builtins.print')
def test_authenticate_with_provided_league_details(mock_print, mock_query_class, mock_load_env, mock_league):
    # Setup
    mock_query_instance = Mock()
    mock_query_class.return_value = mock_query_instance

    # Call function
    authenticate_and_initialize_yf_query(league_details=mock_league)

    # Assert _load_league_details_from_env was NOT called
    mock_load_env.assert_not_called()

    # Assert correct initialization
    mock_query_class.assert_called_once_with(
        league_id="123",
        game_code="nfl",
        game_id="449",
        env_var_fallback=True,
        env_file_location=Path("./env"),
        save_token_data_to_env_file=True,
    )

    mock_print.assert_called_with("Successfully authenticated and initialized Yahoo Fantasy Sports Query.")


# Test 3: Exception during initialization → prints error
@patch('yahoo_fantasy.league.YahooFantasySportsQuery')
@patch('builtins.print')
def test_authenticate_handles_exception(mock_print, mock_query_class, mock_league):
    # Setup
    mock_query_class.side_effect = Exception("Auth failed!")

    # Call function
    authenticate_and_initialize_yf_query(league_details=mock_league)

    # Assert query class was called
    mock_query_class.assert_called_once()

    # Assert error message was printed
    mock_print.assert_called_with("Error: Auth failed!")
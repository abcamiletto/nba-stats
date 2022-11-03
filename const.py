import pathlib

# year: second half of the season - ex. 2010 --> 2009-10
START_YEAR = 2015
END_YEAR = 2022
OUTPUT_DIR = pathlib.Path() / 'data'
URLS_SUBDIR = 'urls'
PLAYERS_SUBDIR = 'players'
OVERWRITE = True

# dataset textual constants
SEASON = 'season'
URL = 'url'

# Set up constants
BASE_URL = 'https://www.basketball-reference.com'
SEASONS_URL = 'https://www.basketball-reference.com/leagues/NBA_{}_per_game.html'
PLAYER_URL = 'https://www.basketball-reference.com'
import re

import requests
from bs4 import BeautifulSoup

from .utils import expand_page

BASE_URL = "https://www.basketball-reference.com"
SEASONS_URL = "https://www.basketball-reference.com/leagues/NBA_{}_per_game.html"

# Set up regex
re_player = re.compile(r"/players/([a-z])/([a-z]{5})([0-9]{2})\.html")
re_season = re.compile(r"/leagues/NBA_([0-9]{4})_per_game\.html")


# Set up headers
headers = {
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.88 Safari/537.36"
}

# Set up session
session = requests.Session()
session.headers.update(headers)


def get_seasons_url(start_year: int, end_year: int) -> list[str]:
    """Returns a list of links with the seasons on basketball-reference.com"""
    seasons = []
    for year in range(start_year, end_year + 1):
        seasons.append(SEASONS_URL.format(year))
    return seasons


def get_players_url(season_url: str) -> list[str]:
    """Get a list of player links to scrape"""
    players = []

    r = session.get(season_url)
    soup = BeautifulSoup(r.text, "html.parser")
    for a in soup.find_all("a", href=re_player):
        player = a["href"]
        url = BASE_URL + player
        players.append(url)
    return players


def get_player_soup(player_url: str) -> BeautifulSoup:
    """Given a url, return the player's data as a BeautifulSoup object"""
    r = session.get(player_url)
    soup = BeautifulSoup(r.text, "html.parser")
    expand_page(soup)
    return soup

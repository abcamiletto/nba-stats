import logging
import re

import chromedriver_autoinstaller
from bs4 import BeautifulSoup
from selenium import webdriver

logging.basicConfig(
    filename="log.txt",
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
)

BASE_URL = "https://www.basketball-reference.com"
SEASONS_URL = "https://www.basketball-reference.com/leagues/NBA_{}_per_game.html"

def expand_page(soup):
    try:
        soup.find("button", {"id": "meta_more_button"}).click()
    except:
        pass


# Set up regex
re_player = re.compile(r"/players/([a-z])/([a-z]{3,9})([0-9]{2})\.html")
re_season = re.compile(r"/leagues/NBA_([0-9]{4})_per_game\.html")


# Set up selenium
chromedriver_autoinstaller.install()
options = webdriver.ChromeOptions()
driver = webdriver.Chrome(options=options)


def get_seasons_url(start_year: int, end_year: int) -> list[str]:
    """Returns a list of links with the seasons on basketball-reference.com"""
    seasons = []
    for year in range(start_year, end_year + 1):
        seasons.append(SEASONS_URL.format(year))

    logging.info(f"Found {len(seasons)} seasons")
    return seasons


def get_players_url(season_url: str) -> list[str]:
    """Get a list of player links to scrape"""
    players = []

    # Opening link with selenium and waiting for it to load
    driver.get(season_url)
    soup = BeautifulSoup(driver.page_source, "html.parser")

    for a in soup.find_all("a", href=re_player):
        player = a["href"]
        url = BASE_URL + player
        players.append(url)

    logging.info(f"Found {len(players)} players")
    return list(set(players))


def get_player_soup(player_url: str) -> BeautifulSoup:
    """Given a url, return the player's data as a BeautifulSoup object"""
    # Opening link with selenium and waiting for it to load
    driver.get(player_url)
    soup = BeautifulSoup(driver.page_source, "html.parser")
    expand_page(soup)
    logging.info(f"Got soup for {player_url}")
    return soup

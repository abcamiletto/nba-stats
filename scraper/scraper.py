import datetime
import logging
import re

from bs4 import BeautifulSoup, Comment

from .utils import find_text_of_p_with


def get_player_stats(soup: BeautifulSoup, season: str) -> dict:
    """Get the player stats"""
    info = {}
    for tr in soup.find_all("tr"):
        tr_season = tr.find("th", {"data-stat": "season"})
        if tr_season is not None:
            if tr_season.text == season:
                for td in tr.find_all("td"):
                    info[td["data-stat"]] = td.text

    if not info:
        logging.warning(f"Could not find stats for season {season}")

    return info


def get_player_seasons(soup: BeautifulSoup, **kwargs) -> list[str]:
    """Get the player seasons"""

    seasons = []
    for tr in soup.find_all("tr"):
        if tr.find("th", {"data-stat": "season"}) is not None:
            season = tr.find("th", {"data-stat": "season"}).text
            # If it is formatted like 2019-20, then it's a season
            if "-" in season:
                seasons.append(season)

    # Remove duplicates
    return list(set(seasons))


def get_player_games(soup: BeautifulSoup, **kwargs) -> dict:
    """Get the player games"""

    games = []
    for tr in soup.find_all("tr"):
        if tr.find("th", {"data-stat": "game_num"}) is not None:
            game = {}
            for td in tr.find_all("td"):
                game[td["data-stat"]] = td.text
            games.append(game)
    return games


def get_player_name(soup: BeautifulSoup, **kwargs) -> str:
    """Get the player name"""
    divs = soup.find("div", {"id": "meta"}).findAll("div")
    div = divs[1] if len(divs) > 1 else divs[0]
    res = div.find("h1").find("span")

    if res is None:
        logging.warning("Could not find player name")

    return res.text


def get_player_height(soup: BeautifulSoup, **kwargs) -> int:
    """Get the player height"""
    # Find any nested <p> with 'cm,' inside
    ps = soup.findAll("p")
    for p in ps:
        if "cm," in p.text:
            return int(p.text.split("cm,")[0][-3:])

    # If we get here, we could not find the height
    logging.warning("Could not find player height")


def get_player_weight(soup: BeautifulSoup, **kwargs) -> int:
    """Get the player weight"""
    # Find any nested <p> with 'cm,' inside
    ps = soup.findAll("p")
    for p in ps:
        if "cm," in p.text:
            return int(p.text.split("kg)")[0][-3:])

    # If we get here, we could not find the weight
    logging.warning("Could not find player weight")


def get_player_birth_date(soup: BeautifulSoup, **kwargs) -> datetime.date:
    """Get the player birth date"""
    # Find text of <p> with 'Born' inside
    text = find_text_of_p_with(soup, "Born")

    if text is None:
        logging.warning("Could not find player birth date")
        return None

    str_date = re.search(r"(?<=Born: ).*(\s[0-9]{4})", text)[0]

    # Convert to datetime
    return datetime.datetime.strptime(str_date, "%B %d, %Y").date()


def get_player_birth_place(soup: BeautifulSoup, **kwargs) -> str:
    """Get the player birth place"""
    # Find text of <p> with 'Born' inside
    text = find_text_of_p_with(soup, "Born")

    # Find text after 'in'
    str_birth = re.search(r"(?<=in ).*", text)[0]
    return str_birth


def get_player_college(soup: BeautifulSoup, **kwargs) -> str:
    """Get the player college"""
    # Find text of <p> with 'College' inside
    text = find_text_of_p_with(soup, "College")

    if text is None:
        logging.warning("Could not find college info")
        return None
    elif "College:" in text:
        college = text.split("College: ")[1]
    elif "Colleges:" in text:
        college = text.split("Colleges: ")[1]
    else:
        raise NotImplementedError(f"Could not find college info on {text}")

    return college


def get_player_draft(soup: BeautifulSoup, **kwargs) -> str:
    # Find text of <p> with 'Draft' inside
    text = find_text_of_p_with(soup, "Draft")

    if text is None:
        logging.warning("Could not find draft info")
        return None

    draft = text.split("Draft: ")[1] if text else None
    return draft


def get_player_salary(soup: BeautifulSoup, **kwargs) -> int:
    """Get the player salary"""

    # This info is loaded dynamically with javascript. We need to use selenium to get it
    # Luckily, it is already loaded in the page as a comment, so we can just parse it

    comments = soup.find_all(string=lambda text: isinstance(text, Comment))
    for c in comments:
        t = c.extract()
        if "$" in t and "salary" in t:
            # parse comment as html
            soup_comment = BeautifulSoup(t, "html.parser")

            # Load nested element <td class="right " data-stat="salary" >$Number</td> inside tfoot
            end_table = soup_comment.find("tfoot")

            if end_table is not None:
                salary = end_table.find("td", {"data-stat": "salary"}).text
                return int(salary[1:].replace(",", ""))

    # If we get here, we could not find the salary
    logging.warning("Could not find player salary")


def get_player_position(soup: BeautifulSoup, **kwargs) -> str:
    """Get the player position"""

    # Find any nested <p> with 'Position:' inside
    ps = soup.findAll("p")
    for p in ps:
        if "Position:" in p.text:
            # Remove whitespaces and newlines from p.text
            text = " ".join(p.text.split())

            position = text.split("Position: ")[1]
            return position

    # If we get here, we could not find the position
    logging.warning("Could not find player position")


# Regroup functions in a dict
scrap_functions = {
    "name": get_player_name,
    "stats": get_player_stats,
    "seasons": get_player_seasons,
    "games": get_player_games,
    "height": get_player_height,
    "weight": get_player_weight,
    "birth_date": get_player_birth_date,
    "birth_place": get_player_birth_place,
    "college": get_player_college,
    "draft": get_player_draft,
    "salary": get_player_salary,
    "position": get_player_position,
}

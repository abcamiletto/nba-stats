def season_number_from_url(url):
    """Get the season number from a url"""
    return int(url.split("_")[1])


def season_string_from_number(year):
    """Convert a season number to a season string"""
    return f"{year-1}-{str(year)[-2:]}"


# get season number from string (ex. 2010-11 --> 2011)
def season_number_from_string(season):
    return int(season.split("-")[0]) + 1


def season_string_from_url(url):
    """Get the season string from a url"""
    return season_string_from_number(season_number_from_url(url))


def find_text_of_p_with(soup, text, exclude=None):
    """Find the text of a p tag with a specific text"""
    if exclude is None:
        exclude = []

    ps = soup.findAll("p")
    for p in ps:
        # Get the text of the <p> tag without the newlines
        p_text = " ".join(p.text.split())
        if text in p_text:
            if any([e in p_text for e in exclude]):
                continue

            return p_text
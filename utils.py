def season_string(year):
    """Convert a year to a season string"""
    return f"{year-1}-{str(year)[-2:]}"


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
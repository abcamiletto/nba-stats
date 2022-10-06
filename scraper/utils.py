def expand_page(soup):
    try:
        soup.find("button", {"id": "meta_more_button"}).click()
    except:
        pass


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

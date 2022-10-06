def expand_page(soup):
    try:
        soup.find("button", {"id": "meta_more_button"}).click()
    except:
        pass


def find_text_of_p_with(soup, text, exclude=None):
    ps = soup.findAll("p")
    for p in ps:
        if text in p.text:
            if exclude is not None and exclude in p.text:
                continue
            # Return the text of the <p> tag without the newlines
            return " ".join(p.text.split())

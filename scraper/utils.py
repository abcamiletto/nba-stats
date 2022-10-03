def expand_page(soup):
    try:
        soup.find("button", {"id": "meta_more_button"}).click()
    except:
        pass


def find_text_of_p_with(soup, text):
    ps = soup.findAll("p")
    for p in ps:
        if text in p.text:
            # Return the text of the <p> tag without the newlines
            return " ".join(p.text.split())

    # If we get here, we didn't find the text
    raise KeyError(f"Could not find string '{text}' in <p> tags")

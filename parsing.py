import requests

def parse_link(url: str):
    if url.startswith('www.'):
        url = 'http://' + url[4:]

    try:
        return requests.get(url).text
    except:
        raise Exception(f"Url {url} could not be opened")

def parse_text(user_input: str):
    """Returns code took from link or user input"""
    if user_input.startswith('http') or user_input.startswith('www.'):
        return parse_link(user_input)
    return user_input
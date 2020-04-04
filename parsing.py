"""Implementation of different input methods"""

import requests
from bs4 import BeautifulSoup


def parse_github(url):
    try:
        html = requests.get(url).text
        soup = BeautifulSoup(html, 'html.parser')
        raw_button = soup.find('a', {'id': 'raw-url'})

        rel_link = raw_button['href'].replace('/raw', '')

        raw_url = 'http://raw.githubusercontent.com' + rel_link

        return parse_link(raw_url)
    except Exception:
        return None


def parse_link(url: str):
    """Returns code from specified url. Only raw pages are supported right now."""
    if url.startswith('www.'):
        url = 'http://' + url[4:]

    url = url.replace('https://', 'http://')

    if url.startswith('http://github.com/'):
        return parse_github(url)

    try:
        return requests.get(url).text
    except Exception:
        return None


def parse_text(user_input: str):
    """Returns code took from link or user input"""
    if user_input.startswith('http') or user_input.startswith('www.'):
        return parse_link(user_input)
    return user_input

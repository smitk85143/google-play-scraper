import re
import requests
import lxml.html

def _get_attrs(doc, _path, attr):
    return [el.get(attr) for el in doc.xpath(_path)]

def _get_apps(url):
    r = requests.get(url)
    if r.status_code != 200:
        return None

    doc = lxml.html.fromstring(r.content)
    pattern = r"id=(.+)"
    hrefs = _get_attrs(doc, '//a', 'href')
    apps = list([re.search(pattern, el).group(1)
         for el in hrefs if el.startswith('/store/apps/details')])
    return apps

def leaderboard(identifier, start=0, num=24, hl="en", gl="us"):
    """
    Returns a list of apps from the Google Play Leaderboard.
    :param identifier: The identifier of the leaderboard. Must be one of topselling_paid, topselling_free or topgrossing.
    :param start: The index of the first app to fetch.
    :param num: The number of apps to fetch.
    :param hl: The language code (default: en).
    :param gl: The country code (default: us).
    
    :return: A list of app ids.
    """
    if identifier not in ('topselling_paid', 'topselling_free', 'topgrossing'):
        raise Exception("identifier must be topselling_paid or topselling_free or topgrossing")

    url = 'https://play.google.com/store/apps'

    url += "/collection/%s?start=%s&num=%s&hl=%s&gl=%s" % (identifier, start, num, hl, gl)
    return _get_apps(url)
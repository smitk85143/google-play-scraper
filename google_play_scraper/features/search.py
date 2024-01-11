import json
from typing import Any, Dict, List
from urllib.parse import quote
import re

from google_play_scraper.constants.element import ElementSpecs
from google_play_scraper.constants.regex import Regex
from google_play_scraper.constants.request import Formats
from google_play_scraper.exceptions import NotFoundError
from google_play_scraper.utils.request import get
from google_play_scraper.features.app import app as app_data


def search(
    query: str, n_hits: int = 50, lang: str = "en", country: str = "us"
) -> List[Dict[str, Any]]:
    query = quote(query)
    url = Formats.Searchresults.build(query=query, lang=lang, country=country)
    try:
        dom = get(url)
    except NotFoundError:
        url = Formats.Searchresults.fallback_build(query=query, lang=lang)
        dom = get(url)

    matches = Regex.SCRIPT.findall(dom)

    dataset = {}

    for match in matches:
        key_match = Regex.KEY.findall(match)
        value_match = Regex.VALUE.findall(match)

        if key_match and value_match:
            key = key_match[0]
            value = json.loads(value_match[0])
            dataset[key] = value

    success = False
    # different idx for different countries and languages
    for idx in range(len(dataset["ds:4"][0][1])):
        try:
            dataset = dataset["ds:4"][0][1][idx][22][0]
            success = True
        except Exception:
            pass
    if not success:
        return []

    n_apps = min(len(dataset), n_hits)
    search_results = []
    try:
        long_string = matches[7][1300:1500]
        app_id_pattern = re.compile(r'https://play.google.com/store/apps/details([^"&]+)')

        # Find all matches in the string
        main_app = app_id_pattern.findall(long_string)[0].split("?id\\u003d")[1]
        app_result = app_data(main_app, lang=lang, country=country)
        app = {}
        app['trackCensoredName'] = main_app
        app['icon'] = app_result['icon']
        app['screenshots'] = app_result['screenshots']
        app['title'] = app_result['trackCensoredName']
        app['averageUserRating'] = app_result['averageUserRating']
        app['genre'] = app_result['genre']
        app['price'] = app_result['price']
        app['free'] = app_result['free']
        app['currency'] = app_result['currency']
        app['video'] = app_result['video']
        app['videoImage'] = app_result['videoImage']
        app['description'] = app_result['description']
        app['descriptionHTML'] = app_result['descriptionHTML']
        app['sellerName'] = app_result['sellerName']
        app['installs'] = app_result['installs']
        search_results.append(app)
    except:
        pass
    for app_idx in range(n_apps):
        app = {}
        for k, spec in ElementSpecs.Searchresult.items():
            content = spec.extract_content(dataset[app_idx])
            app[k] = content
        search_results.append(app)

    return search_results
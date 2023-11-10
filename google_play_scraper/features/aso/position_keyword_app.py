from typing import Any, Dict, List
import yake

from google_play_scraper.features.app import app
from google_play_scraper.features.collection import collection
from google_play_scraper.features.search import search

def conteins_keywords(keywords:List[tuple], key:str) -> bool:
    for k in keywords:
        if(k[0] == key):
            return True
    return False

def position_validator(keywords, app_id, lang, country):
    relevant_keys = []
    for i, key in enumerate(keywords):
        search_result = [ x['appId'] for x in search(key[0], n_hits=50, lang=lang, country=country) ]
        for j, search_app in enumerate(search_result):
            if search_app == app_id:
                relevant_keys.append([key[0], key[1], j+1])
    return relevant_keys

def position_keyword_app(app_id: str, lang: str = "en", country: str = "us", keywords: list = None) -> Dict[str, Any]:
    if keywords is None:
        data = app(app_id, lang, country)
        full_content = [ f"{data['title']} {data['summary']} {data['description']} {data['comments'][0]}{data['comments'][1]}{data['comments'][2]} {data['developer']}" ]

        similar_apps = collection(data['similarAppsPage']['token'], lang, country)['apps']

        # for i, similar_app in enumerate(similar_apps):
        #     if i < 3:
        #         similar_data = app(similar_app, lang, country)
        #         str_content = [f"{similar_data['title']} {similar_data['summary']} {similar_data['description']} {similar_data['developer']}"]
        #         full_content.append(str_content)

        keywords = []
        for txt in full_content:
            extractor = yake.KeywordExtractor(lan=lang, n=3, dedupLim=0.9, features=None, top=50)
            keys = extractor.extract_keywords(txt)
            for k in keys:
                if not conteins_keywords(keywords, k[0]):
                    keywords.append(k)
    else:
        keywords = [(keyword, None) for keyword in keywords]

    position_keywords = position_validator(keywords, app_id, lang, country)

    data = []
    for item in position_keywords:
        data.append({'Key': item[0], "Search position": item[2]})
    data = sorted(data, key=lambda k: k['Search position'])

    return data
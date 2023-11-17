from google_play_scraper.features.aso.scores.difficulty import build as build_difficulty
from google_play_scraper.features.aso.scores.traffic import build as build_traffic
from google_play_scraper.features.aso.utils.gplay import build_store
from google_play_scraper.features.search import search

def score(keyword: str, lang: str = "en", country: str = "us"):
    appsId = [ single_app['appId'] for single_app in search(keyword, n_hits=50, lang=lang, country=country)]
    difficulty = build_difficulty(build_store())(keyword, appsId, lang, country)
    traffic = build_traffic(build_store())(keyword, appsId, lang, country)
    return {
        'difficulty': difficulty,
        'traffic': traffic
    }
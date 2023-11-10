from google_play_scraper.features.search import search
from google_play_scraper.features.app import app as app_info
from google_play_scraper.features.collection import collection
from google_play_scraper.features.leaderboard import leaderboard
from google_play_scraper.features.suggest_keyword import suggest_keyword

from calc import *

MAX_KEYWORD_LENGTH = 25
MAX_SEARCH = 250
MAX_LIST = 50

def get_collection(app):
    return 'TOP_FREE' if app_info(app)['free'] else 'TOP_PAID'

def get_genre(app):
    return app_info(app)['genreId']

def build_store():

    def get_suggest_length(keyword, length=None):
        length = length or 1
        if length > min(len(keyword), MAX_KEYWORD_LENGTH):
            return {'length': None, 'index': None}

        prefix = keyword[:length]
        suggestions = suggest_keyword(prefix)
        index = suggestions.index(keyword) if keyword in suggestions else -1
        
        if index == -1:
            return get_suggest_length(keyword, length + 1)

        return {'length': length, 'index': index}

    def get_installs_score(apps):
        min_installs = [app_info(app)['minInstalls'] for app in apps]
        avg = sum(min_installs) / len(apps)
        max = 1000000
        score = z_score(max, avg)
        return {'avg': avg, 'score': score}

    def get_suggest_score(keyword):
        length_stats = get_suggest_length(keyword)

        if not length_stats['length']:
            score = 1
        else:
            length_score = i_score(1, MAX_KEYWORD_LENGTH, length_stats['length'])
            index_score = iz_score(4, length_stats['index'])
            score = aggregate([10, 1], [length_score, index_score])

        return {**length_stats, 'score': score}

    store = {
        'MAX_SEARCH': 250,
        'MAX_LIST': 50,
        'list': leaderboard,
        'search': search,
        'app': app_info,
        'similar': collection,
        'suggest': get_suggest_length,
        'getInstallsScore': get_installs_score,
        'getSuggestScore': get_suggest_score,
        'getCollection': get_collection,
        'getGenre': get_genre,
        'getCollectionQuery': lambda app: {
            'collection': get_collection(app),
            'category': get_genre(app),
            'num': store['MAX_LIST']
        }
    }

    return store
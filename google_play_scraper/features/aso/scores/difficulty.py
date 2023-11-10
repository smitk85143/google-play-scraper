from datetime import datetime
import yake

from google_play_scraper.features.aso.utils.calc import *
from google_play_scraper.features.app import app as app_info

# Weights to merge all stats into a single score
TITLE_W = 4
COMPETITOR_W = 3
INSTALLS_W = 5
RATING_W = 2
AGE_W = 1

def build(store):
    def get_match_type(keyword, title):
        keyword = keyword.lower()
        title = title.lower()

        if keyword in title:
            return 'exact'

        matches = [title_word in keyword.split(' ') for title_word in title.split(' ')]

        if all(matches):
            return 'broad'
        if any(matches):
            return 'partial'

        return 'none'

    def get_title_matches(keyword, apps):
        matches = [get_match_type(keyword, app_info(app)['title']) for app in apps]
        counts = {
            'exact': matches.count('exact'),
            'broad': matches.count('broad'),
            'partial': matches.count('partial'),
            'none': matches.count('none')
        }
        score = (10 * counts['exact'] + 5 * counts['broad'] + 2.5 * counts['partial']) / len(apps)
        return {'score': score, **counts}
    
    def get_keywords(store):
        def get_keywords(app):
            data = store['app'](app)
            keywords = yake.KeywordExtractor(top=50).extract_keywords(f"{data['summary']} {data['description']}")
            return [keyword[0] for keyword in keywords]
        return get_keywords

    def is_competitor(keyword, app):
        return keyword in get_keywords(store)(app)

    def get_competitors(keyword, apps):
        competitors = [is_competitor(keyword, app) for app in apps]
        count = competitors.count(True)
        score = z_score(len(apps), count)
        return {'count': count, 'score': score}

    def get_rating(keyword, apps):
        avg = sum([app_info(app)['score'] or 0 for app in apps]) / len(apps)
        return {
            'avg': avg,
            'score': avg * 2
        }

    def get_days_since(date):
        if isinstance(date, str):
            date = datetime.fromisoformat(date)  # Assuming the date string is in ISO format (e.g., '2023-11-06T00:00:00')
        else:
            date = datetime.fromtimestamp(date)
        
        current_date = datetime.now()
        delta = current_date - date
        return delta.days

    def get_age(keyword, apps):
        updated = [get_days_since(app_info(app)['updated']) for app in apps]
        avg = sum(updated) / len(apps)
        max = 500
        score = z_score(max, avg)
        return {
            'avgDaysSinceUpdated': avg,
            'score': score
        }

    def get_score(stats):
        return aggregate([TITLE_W, COMPETITOR_W, INSTALLS_W, RATING_W, AGE_W],
                             [stats['titleMatches']['score'], stats['competitors']['score'],
                              stats['installs']['score'], stats['rating']['score'], stats['age']['score']])
    
    def get_installs_score(apps):
        min_installs = [app_info(app)['minInstalls'] for app in apps]
        avg = sum(min_installs) / len(apps)
        max = 1000000
        score = z_score(max, avg)
        return {'avg': avg, 'score': score}

    def get_stats(keyword, apps):
        competitors = get_competitors(keyword, apps)
        top_apps = apps[:10]
        title_matches = get_title_matches(keyword, top_apps)
        installs = get_installs_score(top_apps)
        rating = get_rating(keyword, top_apps)
        age = get_age(keyword, top_apps)
        stats = {
            'titleMatches': title_matches,
            'competitors': competitors,
            'installs': installs,
            'rating': rating,
            'age': age
        }
        stats['score'] = get_score(stats)
        return stats

    return get_stats
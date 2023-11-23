from typing import Any, Dict, List

from google_play_scraper.features.search import search

def search_ids(
    query: str, n_hits: int = 50, lang: str = "en", country: str = "us"
) -> List[Dict[str, Any]]:
    results = search(query, n_hits, lang, country)
    return [result["trackCensoredName"] for result in results]
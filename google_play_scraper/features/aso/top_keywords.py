from typing import Dict, Any

from google_play_scraper.features.suggest_keyword import suggest_keyword

def top_keywords(country: str = "us") -> Dict[str, Any]:
    """
    Get top keywords for a country
    :param country: two letter country code

    Note: This function is only support english language
    """
    alphabet = "abcdefghijklmnopqrstuvwxyz"
    map_popularity = {}
    for char in alphabet:
        suggests = suggest_keyword(char, country=country)
        minus = 0
        for s in suggests:
            map_popularity[s] = 6 - minus
            minus += 1

    data = []

    for item in map_popularity.items():
        data.append({'Key': item[0], "Relative popularity": item[1]})

    data = sorted(data, key=lambda k: k['Relative popularity'], reverse=True)

    return data
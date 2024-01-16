from typing import Union
from urllib.error import HTTPError
from urllib.request import Request, urlopen

from google_play_scraper.exceptions import (
    NotFoundError,
    ExtraHTTPError,
    TooManyRequestsError,
)

def _urlopen(obj, timeout):
    try:
        resp = urlopen(obj, timeout=timeout)
    except HTTPError as e:
        if e.code == 404:
            raise NotFoundError("Page not found(404).")
        elif e.code == 429:
            raise TooManyRequestsError("Too many requests(429).")
        else:
            raise ExtraHTTPError(
                "Page not found. Status code {} returned.".format(e.code)
            )

    return resp.read().decode("UTF-8")


def post(url: str, data: Union[str, bytes], headers: dict) -> str:
    return _urlopen(Request(url, data=data, headers=headers))


def get(url: str, herder: str = None, timeout: int = 2) -> str:
    if herder != None:
        return _urlopen(Request(url, herder=herder), timeout=timeout)
    return _urlopen(url, timeout=timeout)

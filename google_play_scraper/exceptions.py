class GooglePlayScraperException(Exception):
    pass


class NotFoundError(GooglePlayScraperException):
    pass


class ExtraHTTPError(GooglePlayScraperException):
    pass

class TooManyRequestsError(GooglePlayScraperException):
    pass
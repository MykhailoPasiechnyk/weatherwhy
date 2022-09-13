class RequestError(Exception):
    pass


class TitleCityException(RequestError):
    """Raised when weather API return BAD REQUEST"""
    pass

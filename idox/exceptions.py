class BaseIdoxException(Exception):
    """Base exception class"""

    def __init__(self, *args):
        self.message = args[0] if args else self.__doc__

    def __str__(self):
        return self.message


class MalformedRequest(BaseIdoxException):
    """The provided request did not match the excepted HTTP format."""

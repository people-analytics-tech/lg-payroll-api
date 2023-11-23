from enum import Enum


class LGStatus(Enum):
    SUCCESS = 0
    INCONSISTENCE = 1
    ERROR = 2
    NOT_PROCESS = 3


class LgException(Exception):
    def __init__(self, message: str) -> None:
        super().__init__(message)


class LgInconsistencyException(LgException):
    def __init__(self, message: str) -> None:
        super().__init__(f"LG INCONSISTENCY - {message}")


class LgErrorException(LgException):
    def __init__(self, message: str) -> None:
        super().__init__(f"LG ERROR - {message}")


class LgNotProcessException(LgException):
    def __init__(self, message: str) -> None:
        super().__init__(f"LG NOT PROCESS - {message}")

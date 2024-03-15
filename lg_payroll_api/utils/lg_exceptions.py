class LgException(Exception):
    def __init__(self, message: str) -> None:
        super().__init__(message)


class LgParameterListLimitException(LgException):
    def __init__(self, message: str) -> None:
        super().__init__(f"ERROR - {message}")


class LgInconsistencyException(LgException):
    def __init__(self, message: str) -> None:
        super().__init__(f"LG INCONSISTENCY - {message}")


class LgErrorException(LgException):
    def __init__(self, message: str) -> None:
        super().__init__(f"LG ERROR - {message}")


class LgNotProcessException(LgException):
    def __init__(self, message: str) -> None:
        super().__init__(f"LG NOT PROCESS - {message}")

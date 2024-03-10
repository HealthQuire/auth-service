from fastapi import HTTPException, status


class WrongPassword(HTTPException):
    def __init__(self) -> None:
        super().__init__(status_code=status.HTTP_401_UNAUTHORIZED,
                         detail="Wrong password")


class UserNotExist(HTTPException):
    def __init__(self) -> None:
        super().__init__(status_code=status.HTTP_401_UNAUTHORIZED,
                         detail="User not exist")


class TokenExpired(HTTPException):
    def __init__(self) -> None:
        super().__init__(status_code=status.HTTP_401_UNAUTHORIZED,
                         detail="Token is expired")


class InvalidAccessToken(HTTPException):
    def __init__(self) -> None:
        super().__init__(status_code=status.HTTP_401_UNAUTHORIZED,
                         detail="Access token in refresh and real token are not same")

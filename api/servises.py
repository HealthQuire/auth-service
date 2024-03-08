from os import environ
from jose import jwt, JWTError
from datetime import datetime, timedelta
from load_env import load_env

from api import exceptions

load_env()


class TokenProvider:
    _SECRET_KEY = environ.get("SECRET_KEY")
    _ALGORITHM = environ.get("ALGORITHM")
    _ACCESS_TOKEN_EXPIRE_MINUTES = timedelta(
        minutes=int(environ.get("ACCESS_TOKEN_EXPIRE_MINUTES")))
    _REFRESH_TOKEN_EXPIRE_DAYS = timedelta(days=int(environ.get("REFRESH_TOKEN_EXPIRE_HOURS")))

    # TODO: add checking user authorization
    @classmethod
    def _check_authorization(cls, login: str, password: str) -> dict:
        return {"user_id": 1, "user_role": 6}

    @classmethod
    def _create_token(cls, data: dict, expires_delta: timedelta) -> str:
        expire = datetime.utcnow() + expires_delta
        data["exp"] = expire
        encoded_jwt = jwt.encode(data, cls._SECRET_KEY, algorithm=cls._ALGORITHM)
        return encoded_jwt

    @classmethod
    def _create_access_refresh(cls, data: dict):
        access_token = cls._create_token(data, cls._ACCESS_TOKEN_EXPIRE_MINUTES)
        data.update({"access_token": access_token})
        refresh_token = cls._create_token(data, cls._REFRESH_TOKEN_EXPIRE_DAYS)
        return {"access_token": access_token, "refresh_token": refresh_token}

    @classmethod
    def create_tokens(cls, login: str, password: str):
        user_data = cls._check_authorization(login, password)
        return cls._create_access_refresh(user_data)

    @classmethod
    def decode_token(cls, access_token: str):
        try:
            payload = jwt.decode(access_token, cls._SECRET_KEY, algorithms=[cls._ALGORITHM])
        except JWTError:
            raise exceptions.TokenExpired
        user_id = payload.get("user_id")
        user_role = payload.get("user_role")
        if user_id is None or user_role:
            raise exceptions.TokenExpired
        return {"user_id": user_id, "user_role": user_role}

    @classmethod
    def refresh_tokens(cls, access_token: str, refresh_token: str):
        payload = jwt.decode(refresh_token, cls._SECRET_KEY, algorithms=[cls._ALGORITHM])
        if payload.get("access_token") != access_token:
            raise exceptions.InvalidAccessToken
        user_role = payload.get("user_role")
        user_id = payload.get("user_id")
        if user_role is None or user_id is None:
            raise exceptions.InvalidAccessToken
        user_data = {"user_id": user_id, "user_role": user_role}
        return cls._create_access_refresh(user_data)

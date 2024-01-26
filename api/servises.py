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

    @classmethod
    def _create_token(cls, data: dict, expires_delta: timedelta) -> str:
        expire = datetime.utcnow() + expires_delta
        data["exp"] = expire
        encoded_jwt = jwt.encode(data, cls._SECRET_KEY, algorithm=cls._ALGORITHM)
        return encoded_jwt

    @classmethod
    def create_tokens(cls, user_id: int, service_from: str):
        data = {"user_id": user_id, "service_from": service_from}
        access_token = cls._create_token(data, cls._ACCESS_TOKEN_EXPIRE_MINUTES)
        data.update({"access_token": access_token})
        refresh_token = cls._create_token(data, cls._REFRESH_TOKEN_EXPIRE_DAYS)
        return {"access_token": access_token, "refresh_token": refresh_token}

    @classmethod
    def decode_token(cls, service_from: str, access_token: str):
        try:
            payload = jwt.decode(access_token, cls._SECRET_KEY, algorithms=[cls._ALGORITHM])
        except JWTError:
            raise exceptions.TokenExpired
        user_id = payload.get("user_id")
        if user_id is None:
            raise exceptions.TokenExpired
        service_from_token = payload.get("service_from")
        if service_from_token is None or service_from_token != service_from:
            raise exceptions.InvalidServiceFrom
        return {"user_id": user_id, "service_from": service_from}

    @classmethod
    def refresh_tokens(cls, service_from: str, access_token: str, refresh_token: str):
        payload = jwt.decode(refresh_token, cls._SECRET_KEY, algorithms=[cls._ALGORITHM])
        if payload.get("access_token") != access_token:
            raise exceptions.InvalidAccessToken
        service_from_token = payload.get("access_token")
        if service_from_token is None or service_from_token != service_from:
            raise exceptions.InvalidServiceFrom
        return cls.create_tokens(int(payload.get("user_id")), service_from)

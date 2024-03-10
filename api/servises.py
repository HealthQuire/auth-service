from os import environ

import requests
from jose import jwt, JWTError
from datetime import datetime, timedelta
from load_env import load_env

from api import exceptions

load_env()


class TokenProvider:
    _LOGIN_ENDPOINT = environ.get("LOGIN_ENDPOINT")
    _SECRET_KEY = environ.get("SECRET_KEY")
    _ALGORITHM = environ.get("ALGORITHM")
    _ACCESS_TOKEN_EXPIRE_MINUTES = timedelta(
        minutes=int(environ.get("ACCESS_TOKEN_EXPIRE_MINUTES")))
    _REFRESH_TOKEN_EXPIRE_DAYS = timedelta(days=int(environ.get("REFRESH_TOKEN_EXPIRE_HOURS")))

    @classmethod
    def _check_authorization(cls, login: str, password: str) -> dict:
        res = requests.post(cls._LOGIN_ENDPOINT, json={"password": password, "email": login})
        if res.status_code == 500:
            raise exceptions.WrongPassword
        if res.status_code == 404:
            raise exceptions.UserNotExist
        data = res.json()
        return {"user_id": data["id"], "user_role": data["role"]}

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
        if user_id is None or user_role is None:
            raise exceptions.TokenExpired
        return {"user_id": user_id, "user_role": user_role}

    @classmethod
    def refresh_tokens(cls, access_token: str, refresh_token: str):
        try:
            payload = jwt.decode(refresh_token, cls._SECRET_KEY, algorithms=[cls._ALGORITHM])
        except JWTError:
            raise exceptions.TokenExpired
        if payload.get("access_token") != access_token:
            raise exceptions.InvalidAccessToken
        user_role = payload.get("user_role")
        user_id = payload.get("user_id")
        if user_role is None or user_id is None:
            raise exceptions.InvalidAccessToken
        user_data = {"user_id": user_id, "user_role": user_role}
        return cls._create_access_refresh(user_data)

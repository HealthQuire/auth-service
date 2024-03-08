from fastapi import APIRouter, Header

from load_env import load_env
from api import servises

load_env()
auth_router = APIRouter()


@auth_router.post("/create_token")
async def create_wallet(login: str = Header(), password: str = Header()):
    return servises.TokenProvider.create_tokens(login, password)


@auth_router.post("/decode_token")
async def decode_token(access_token: str = Header()):
    return servises.TokenProvider.decode_token(access_token)


@auth_router.post("/refresh_token")
async def refresh_tokens(access_token: str = Header(),
                         refresh_token: str = Header()):
    return servises.TokenProvider.refresh_tokens(access_token, refresh_token)

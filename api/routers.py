from fastapi import APIRouter, Header

from load_env import load_env
from api import servises

load_env()
auth_router = APIRouter()


@auth_router.post("/create_token")
async def create_wallet(user_id: int = Header(), service_from: str = Header()):
    return servises.TokenProvider.create_tokens(user_id, service_from)

#
# load_env()
# _CODE_EXPIRES = timedelta(seconds=int(environ.get("CODE_EXPIRES")))
# PWD_CONTEXT = CryptContext(schemes=["bcrypt"], deprecated="auto")
# ACCESS_TOKEN_EXPIRE_MINUTES = timedelta(minutes=int(environ.get("ACCESS_TOKEN_EXPIRE_MINUTES")))
# REFRESH_TOKEN_EXPIRE_HOURS = timedelta(days=int(environ.get("REFRESH_TOKEN_EXPIRE_DAYS")))
# SECRET_KEY =
# ALGORITHM = environ.get("ALGORITHM")
# SMS_TOKEN = "maqvdiops8pqq3g12xpnra1ldl3gaxe0v4s3ay90hnt5qbykh74uafjhchripgrv"
#
#
# def _get_sms_code(phone: str) -> str:
#     code = ''.join(map(str, random.choices(range(10), k=4)))
#     body = {"messages": [{"recipient": phone,
#                           "recipientType": "recipient",
#                           "source": "Portal VR",
#                           "timeout": 3600,
#                           "text": f"Ваш код авторизации в приложении Portal VR: {code}"}]}
#     resp = requests.post("https://lcab.smsint.ru/json/v1.0/sms/send/text",
#                          headers={"X-Token": SMS_TOKEN},
#                          json=body).json()
#     return code
#
#
# def _create_token(data: dict, expires_delta: timedelta) -> str:
#     expire = datetime.utcnow() + expires_delta
#     data["exp"] = expire
#     encoded_jwt = jwt.encode(data, SECRET_KEY, algorithm=ALGORITHM)
#     return encoded_jwt
#
#
# def hash_pincode(pincode: str) -> str:
#     return PWD_CONTEXT.hash(pincode)
#
#
# def send_code_to_user(user: User, session: Session) -> None:
#     # send sms code to user and write it to database
#     if user.sms_code_update_at is not None:
#         if datetime.now() < user.sms_code_update_at:
#             raise SMSError(f"Wait until {str(user.sms_code_update_at)} to update sms code")
#     code = _get_sms_code(user.phone)
#     user.sms_code = code
#     user.sms_code_update_at = datetime.now() + _CODE_EXPIRES
#     session.commit()
#     session.refresh(user)
#
#
# def verify_code(user: User, sms_code: str, session: Session) -> None:
#     if user.sms_code is None:
#         raise SMSError("Sms code wasn't sent to user")
#     if sms_code != "1111" and user.sms_code != sms_code:
#         raise SMSError("Sms code incorrect")
#     user.sms_code = None
#     user.sms_code_update_at = None
#     user.can_change_pincode = True
#     user.activated = True
#     session.commit()
#
#
# def authorization_user(user: User, pincode: str) -> dict:
#     if not PWD_CONTEXT.verify(pincode, user.hashed_pincode):
#         raise UserError("Incorrect pincode")
#     access_token_data = {"sub": str(user.id)}
#     access_token = _create_token(access_token_data, ACCESS_TOKEN_EXPIRE_MINUTES)
#     refresh_token = _create_token({"sub": str(user.id), "access": access_token},
#                                   REFRESH_TOKEN_EXPIRE_HOURS)
#     return {"access_token": access_token, "refresh_token": refresh_token, "user": user}
#
#
# def decode_token(token: str) -> int:
#     try:
#         payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
#         user_id: int = int(payload.get("sub"))
#         if user_id is None:
#             raise TokenError("Invalid credentials")
#         return user_id
#     except JWTError:
#         raise TokenError("Token expired")
#
#
# def update_access_token(access_token: str, refresh_token: str):
#     payload = jwt.decode(refresh_token, SECRET_KEY, algorithms=[ALGORITHM])
#     if payload.get("access") != access_token:
#         raise TokenError("Refresh token not from this access token")
#     access_token = _create_token({"sub": payload.get("sub")}, ACCESS_TOKEN_EXPIRE_MINUTES)
#     refresh_token = _create_token({"sub": payload.get("sub"), "access": access_token},
#                                   REFRESH_TOKEN_EXPIRE_HOURS)
#     return {"access_token": access_token, "refresh_token": refresh_token}
#
#
# if __name__ == '__main__':
#     print(_get_sms_code("89004951127"))

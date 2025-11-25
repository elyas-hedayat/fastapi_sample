import time
from datetime import datetime, timedelta

import jwt

JWT_SECRET = ""
JWT_ALGORITHM = "HS256"


def token_response(token: str):
    return {"access_token": token}


def sign_jwt(user_id: int):
    payload = {"exp": time.time() + 3600, "id": user_id}
    token = jwt.encode(payload, JWT_SECRET, algorithm=JWT_ALGORITHM)
    return token_response(token)


def decode_jwt(token: str):
    try:
        decode_token = jwt.decode(token, JWT_SECRET, algorithms=[JWT_ALGORITHM])
        return decode_token if decode_token else None
    except:
        return {}

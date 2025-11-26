from typing import Annotated

import jwt
from fastapi import Depends, HTTPException, status
from jwt import PyJWTError
from sqlmodel import Session
from database import get_session
from jwt_auth import JWT_SECRET, JWT_ALGORITHM
from models.hero import Hero
from passlib.context import CryptContext
from fastapi.security import HTTPBearer

from models.user import User

oauth2_scheme = HTTPBearer()

SessionDep = Annotated[Session, Depends(get_session)]

password_context = CryptContext(schemes=["sha256_crypt"])


class Hasher:
    @staticmethod
    def verify_password(plain_password, hashed_password):
        return password_context.verify(plain_password, hashed_password)

    @staticmethod
    def get_password_hash(plain_password):
        return password_context.hash(plain_password)

def get_hero_or_404(session: Session, hero_id: int) -> Hero:
    hero = session.get(Hero, hero_id)
    if not hero:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Hero not found")
    return hero


def verify_jwt_token(token: str):
    try:
        payload = jwt.decode(token, JWT_SECRET, algorithms=[JWT_ALGORITHM])
        user_id: int = int(payload.get("id"))
        if user_id is None:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Could not validate credentials",
                headers={"WWW-Authenticate": "Bearer"},
            )
        return user_id
    except PyJWTError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )


def get_current_user(
        credentials=Depends(oauth2_scheme),
        db: Session = Depends(get_session)
):
    token = credentials.credentials  # the actual raw JWT
    print(token)
    user_id = verify_jwt_token(token)
    user = db.query(User).filter(User.id == user_id).first()
    if user is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    return user

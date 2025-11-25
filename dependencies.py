from typing import Annotated
from fastapi import Depends, HTTPException, status
from sqlmodel import Session
from database import get_session
from models.hero import Hero
from passlib.context import CryptContext
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

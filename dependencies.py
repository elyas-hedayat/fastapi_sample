from typing import Annotated
from fastapi import Depends, HTTPException, status
from sqlmodel import Session
from database import get_session
from models.hero import Hero

SessionDep = Annotated[Session, Depends(get_session)]


def get_hero_or_404(session: Session, hero_id: int) -> Hero:
    hero = session.get(Hero, hero_id)
    if not hero:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Hero not found")
    return hero

from typing import Annotated

from fastapi import APIRouter, status, Query
from sqlmodel import select

from dependencies import SessionDep
from models.hero import Hero
from schemas.hero import HeroCreate, HeroResponse, HeroUpdate

router = APIRouter()


@router.post("/heroes/", status_code=status.HTTP_201_CREATED, response_model=HeroResponse)
def create_heroes(hero: HeroCreate, session: SessionDep):
    instance = Hero.model_validate(hero)
    session.add(instance)
    session.commit()
    session.refresh(instance)
    return {"message": "Hero created successfully", "hero": instance}


@router.get("/heroes/", status_code=status.HTTP_200_OK, response_model=list[Hero])
def read_heroes(
        session: SessionDep,
        offset: int = 0,
        limit: Annotated[int, Query(le=100)] = 100,
):
    heroes = session.exec(select(Hero).offset(offset).limit(limit)).all()
    return heroes


@router.get("/heroes/{hero_id}", status_code=status.HTTP_200_OK, response_model=Hero)
def get_hero(hero_id: int, session: SessionDep):
    return get_hero_or_404(session, hero_id)


@router.delete("/heroes/{hero_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_hero(hero_id: int, session: SessionDep):
    instance = get_hero_or_404(session, hero_id)
    session.delete(instance)
    session.commit()


@router.patch("/heroes/{hero_id}", response_model=HeroResponse)
def update_hero(hero_id: int, hero: HeroUpdate, session: SessionDep, ):
    instance = get_hero_or_404(session, hero_id)
    hero_data = hero.model_dump(exclude_unset=True)
    instance.sqlmodel_update(hero_data)
    session.add(instance)
    session.commit()
    session.refresh(instance)
    return {"message": "Hero updated successfully", "hero": hero}

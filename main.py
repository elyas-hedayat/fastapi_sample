from typing import Annotated

from fastapi import Depends, FastAPI, HTTPException, Query, status
from sqlmodel import Field, Session, SQLModel, create_engine, select


class HeroBase(SQLModel):
    name: str
    secret_name: str
    age: int | None = None


class HeroCreate(HeroBase):
    pass


class HeroUpdate(SQLModel):
    name: str | None = None
    secret_name: str | None = None
    age: int | None = None


class HeroPublic(HeroBase):
    id: int


class HeroResponse(SQLModel):
    message: str
    hero: HeroPublic


class Hero(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    name: str = Field(index=True)
    age: int | None = Field(default=None, index=True)
    secret_name: str


sqlite_file_name = "database.db"
sqlite_url = f"sqlite:///{sqlite_file_name}"

connect_args = {"check_same_thread": False}
engine = create_engine(sqlite_url, connect_args=connect_args)


def create_db_and_tables():
    SQLModel.metadata.create_all(engine)


def get_session():
    with Session(engine) as session:
        yield session


SessionDep = Annotated[Session, Depends(get_session)]

app = FastAPI()


@app.on_event("startup")
def on_startup():
    create_db_and_tables()


def get_hero_or_404(session: Session, hero_id: int) -> Hero:
    hero = session.get(Hero, hero_id)
    if not hero:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Hero not found")
    return hero


@app.post("/heroes/", status_code=status.HTTP_201_CREATED, response_model=HeroResponse)
def create_heroes(hero: HeroCreate, session: SessionDep):
    instance = Hero.model_validate(hero)
    session.add(instance)
    session.commit()
    session.refresh(instance)
    return {"message": "Hero created successfully", "hero": instance}


@app.get("/heroes/", status_code=status.HTTP_200_OK, response_model=list[Hero])
def read_heroes(
        session: SessionDep,
        offset: int = 0,
        limit: Annotated[int, Query(le=100)] = 100,
):
    heroes = session.exec(select(Hero).offset(offset).limit(limit)).all()
    return heroes


@app.get("/heroes/{hero_id}", status_code=status.HTTP_200_OK, response_model=Hero)
def get_hero(hero_id: int, session: SessionDep):
    return get_hero_or_404(session, hero_id)


@app.delete("/heroes/{hero_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_hero(hero_id: int, session: SessionDep):
    instance = get_hero_or_404(session, hero_id)
    session.delete(instance)
    session.commit()


@app.patch("/heroes/{hero_id}", response_model=HeroResponse)
def update_hero(hero_id: int, hero: HeroUpdate, session: SessionDep, ):
    instance = get_hero_or_404(session, hero_id)
    hero_data = hero.model_dump(exclude_unset=True)
    instance.sqlmodel_update(hero_data)
    session.add(instance)
    session.commit()
    session.refresh(instance)
    return {"message": "Hero updated successfully", "hero": hero}

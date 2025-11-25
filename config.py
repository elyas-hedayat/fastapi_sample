from fastapi import FastAPI

from database import create_db_and_tables
from routers import hero, user

app = FastAPI()

app.include_router(hero.router, tags=['Hero'])
app.include_router(user.router, tags=['user'])


@app.on_event('startup')
def on_startup():
    create_db_and_tables()

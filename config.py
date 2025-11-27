from fastapi import FastAPI

from database import create_db_and_tables
from routers import hero, user, crypto_token

app = FastAPI()

app.include_router(hero.router, tags=['Hero'])
app.include_router(user.router, tags=['user'])
app.include_router(crypto_token.router, tags=['crypto_token'])


@app.on_event('startup')
def on_startup():
    create_db_and_tables()

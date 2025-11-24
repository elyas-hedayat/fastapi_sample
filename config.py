from fastapi import FastAPI
from routers import hero

app = FastAPI()

app.include_router(hero.router, tags=['Hero'])

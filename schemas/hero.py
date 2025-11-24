from pydantic import BaseModel


class HeroBase(BaseModel):
    name: str
    secret_name: str
    age: int | None = None


class HeroCreate(HeroBase):
    pass


class HeroUpdate(BaseModel):
    name: str | None = None
    secret_name: str | None = None
    age: int | None = None


class HeroPublic(HeroBase):
    id: int


class HeroResponse(BaseModel):
    message: str
    hero: HeroPublic

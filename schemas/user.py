from pydantic import BaseModel, Field


class RegisterInput(BaseModel):
    username: str = Field(..., max_length=125)
    password: str


class RegisterOutput(RegisterInput):
    id: int

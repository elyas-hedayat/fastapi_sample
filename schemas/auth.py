from pydantic import BaseModel


class ChangePasswordInput(BaseModel):
    current_password: str
    new_password: str

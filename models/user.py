from sqlmodel import SQLModel, Field


class User(SQLModel, table=True):
    __tablename__ = "user"

    id: int | None = Field(default=None, primary_key=True)
    username: str = Field(index=True, max_length=125)
    password: str = Field(max_length=255)

    def __repr__(self):
        return f"<{self.__class__}({self.username})>"

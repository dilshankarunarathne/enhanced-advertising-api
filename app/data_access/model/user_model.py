from pydantic import BaseModel


"""
This module defines the data models used by the API.

"""
class User(BaseModel):
    id: int
    username: str | None = None
    email: str | None = None
    is_adviser: bool | None = None


class UserInDB(User):
    hashed_password: str

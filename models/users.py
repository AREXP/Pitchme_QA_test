from pydantic import BaseModel
from typing import List


class User(BaseModel):
    id: int
    name: str
    email: str


class UserCreate(BaseModel):
    name: str
    email: str


class UserUpdate(BaseModel):
    name: str
    email: str


class UserList(BaseModel):
    data: List[User]

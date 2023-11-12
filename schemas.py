from pydantic import BaseModel
from typing import List

class User(BaseModel):
    id: int
    name: str
    email: str


class Post(BaseModel):
    id: int
    title: str
    content: str
    user_id: int


class UserCreate(BaseModel):
    name: str
    email: str


class UserUpdate(BaseModel):
    name: str
    email: str


class UserList(BaseModel):
    data: List[User]


class PostCreate(BaseModel):
    title: str
    content: str
    user_id: int


class PostUpdate(BaseModel):
    title: str
    content: str
    user_id: int 


class PostList(BaseModel):
    data: List[Post]

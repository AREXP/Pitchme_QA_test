from pydantic import BaseModel
from typing import List


class Post(BaseModel):
    id: int
    title: str
    content: str
    user_id: int


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

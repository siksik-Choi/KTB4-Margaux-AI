from typing import Optional
from sqlmodel import SQLModel, Field


class Post(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    title: str
    content: str
    author: str
    summary: Optional[str] = None


class PostCreate(SQLModel):
    title: str
    content: str
    author: str


class PostUpdate(SQLModel):
    title: Optional[str] = None
    content: Optional[str] = None
    author: Optional[str] = None


class Comment(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    content: str
    author: str


class CommentCreate(SQLModel):
    content: str
    author: str


class CommentUpdate(SQLModel):
    content: Optional[str] = None
    author: Optional[str] = None

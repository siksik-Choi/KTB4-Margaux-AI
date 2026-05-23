from sqlmodel import SQLModel, Field, Session, create_engine, select
from fastapi import FastAPI
from typing import Optional

from ollama import chat
from ollama import ChatResponse

# Database 설정
DATABASE_URL = "sqlite:///./posts_comments.db"
engine = create_engine(DATABASE_URL, echo=True)

app = FastAPI()

class Post(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    title: str
    content: str
    author: str
    summary: Optional[str] = None

class PostUpdate(SQLModel):
    title: Optional[str] = None
    content: Optional[str] = None
    author: Optional[str] = None

class Comment(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    content: str
    author: str

class CommentUpdate(SQLModel):
    content: Optional[str] = None
    author: Optional[str] = None

# 테이블 생성
SQLModel.metadata.create_all(engine)

@app.post("/posts/")
def create_post(post: Post):
    
    # ollama API를 사용하여 게시물 요약 생성
    response: ChatResponse = chat(model='gemma4:e4b ', messages=[
    {
        'role': 'user',
        'content': '제목: {title}\n내용: {content}\n작성자: {author}\n\n이 게시물의 요약을 3문장으로 작성해줘.'.format(
            title=post.title,
            content=post.content,
            author=post.author
        ),
    },
    ])
    print("summary: " + response['message']['content'])
    
    # 게시물 요약을 Post 객체에 저장
    post.summary = response.message.content
    
    with Session(engine) as session:
        session.add(post)
        session.commit()
        session.refresh(post)
    return post


@app.get("/posts/")
def get_posts():
    with Session(engine) as session:
        posts = session.exec(select(Post)).all()
    return posts


@app.put("/posts/{post_id}")
def update_post(post_id: int, updated_post: Post):
    with Session(engine) as session:
        post = session.get(Post, post_id)
        if not post:
            return {"message": f"{post_id}번 게시물이 없습니다."}
        post.title = updated_post.title
        post.content = updated_post.content
        post.author = updated_post.author
        session.add(post)
        session.commit()
        session.refresh(post)
    return post


@app.patch("/posts/{post_id}")
def patch_post(post_id: int, updated_fields: PostUpdate):
    with Session(engine) as session:
        post = session.get(Post, post_id)
        if not post:
            return {"message": f"{post_id}번 게시물이 없습니다."}
        update_data = updated_fields.model_dump(exclude_unset=True)

        for key, value in update_data.items():
            setattr(post, key, value)
        session.add(post)
        session.commit()
        session.refresh(post)
    return post


@app.delete("/posts/{post_id}")
def delete_post(post_id: int):
    with Session(engine) as session:
        post = session.get(Post, post_id)
        if not post:
            return {"message": f"{post_id}번 게시물이 없습니다."}
        session.delete(post)
        session.commit()
    return {"message": f"{post_id}번 게시물이 삭제되었습니다."}


@app.post("/comments/")
def create_comment(comment: Comment):
    with Session(engine) as session:
        session.add(comment)
        session.commit()
        session.refresh(comment)
    return comment


@app.get("/comments/")
def get_comments():
    with Session(engine) as session:
        comments = session.exec(select(Comment)).all()
    return comments


@app.put("/comments/{comment_id}")
def update_comment(comment_id: int, updated_comment: Comment):
    with Session(engine) as session:
        comment = session.get(Comment, comment_id)
        if not comment:
            return {"message": f"{comment_id}번 댓글이 없습니다."}
        comment.content = updated_comment.content
        comment.author = updated_comment.author
        session.add(comment)
        session.commit()
        session.refresh(comment)
    return comment


@app.patch("/comments/{comment_id}")
def patch_comment(comment_id: int, updated_fields: CommentUpdate):
    with Session(engine) as session:
        comment = session.get(Comment, comment_id)
        if not comment:
            return {"message": f"{comment_id}번 댓글이 없습니다."}
        update_data = updated_fields.model_dump(exclude_unset=True)

        for key, value in update_data.items():
            setattr(comment, key, value)
        session.add(comment)
        session.commit()
        session.refresh(comment)
    return comment


@app.delete("/comments/{comment_id}")
def delete_comment(comment_id: int):
    with Session(engine) as session:
        comment = session.get(Comment, comment_id)
        if not comment:
            return {"message": f"{comment_id}번 댓글이 없습니다."}
        session.delete(comment)
        session.commit()
    return {"message": f"{comment_id}번 댓글이 삭제되었습니다."}


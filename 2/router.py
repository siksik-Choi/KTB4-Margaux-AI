from fastapi import APIRouter, HTTPException
from sqlmodel import Session, select

from ollama import chat, ChatResponse

from database import engine
from models import (
    Post,
    PostCreate,
    PostUpdate,
    Comment,
    CommentCreate,
    CommentUpdate,
)

router = APIRouter()


@router.post("/posts/")
def create_post(post: PostCreate):
    response: ChatResponse = chat(model='gemma4:e4b ', messages=[
        {
            'role': 'user',
            'content': '제목: {title}\n내용: {content}\n작성자: {author}\n\n이 게시물의 요약을 3문장으로 작성해줘.'.format(
                title=post.title,
                content=post.content,
                author=post.author,
            ),
        },
    ])

    post_data = post.model_dump()
    post_data["summary"] = response.message.content
    new_post = Post(**post_data)
    with Session(engine) as session:
        session.add(new_post)
        session.commit()
        session.refresh(new_post)
    return new_post


@router.get("/posts/")
def get_posts():
    with Session(engine) as session:
        posts = session.exec(select(Post)).all()
    return posts


@router.put("/posts/{post_id}")
def update_post(post_id: int, updated_post: Post):
    with Session(engine) as session:
        post = session.get(Post, post_id)
        if not post:
            raise HTTPException(status_code=404, detail=f"{post_id}번 게시물이 없습니다.")
        post.title = updated_post.title
        post.content = updated_post.content
        post.author = updated_post.author
        session.add(post)
        session.commit()
        session.refresh(post)
    return post


@router.patch("/posts/{post_id}")
def patch_post(post_id: int, updated_fields: PostUpdate):
    with Session(engine) as session:
        post = session.get(Post, post_id)
        if not post:
            raise HTTPException(status_code=404, detail=f"{post_id}번 게시물이 없습니다.")
        update_data = updated_fields.model_dump(exclude_unset=True)
        for key, value in update_data.items():
            setattr(post, key, value)
        session.add(post)
        session.commit()
        session.refresh(post)
    return post


@router.delete("/posts/{post_id}")
def delete_post(post_id: int):
    with Session(engine) as session:
        post = session.get(Post, post_id)
        if not post:
            raise HTTPException(status_code=404, detail=f"{post_id}번 게시물이 없습니다.")
        session.delete(post)
        session.commit()
    return {"message": f"{post_id}번 게시물이 삭제되었습니다."}


@router.post("/comments/")
def create_comment(comment: CommentCreate):
    new_comment = Comment(**comment.model_dump())
    with Session(engine) as session:
        session.add(new_comment)
        session.commit()
        session.refresh(new_comment)
    return new_comment


@router.get("/comments/")
def get_comments():
    with Session(engine) as session:
        comments = session.exec(select(Comment)).all()
    return comments


@router.put("/comments/{comment_id}")
def update_comment(comment_id: int, updated_comment: Comment):
    with Session(engine) as session:
        comment = session.get(Comment, comment_id)
        if not comment:
            raise HTTPException(status_code=404, detail=f"{comment_id}번 댓글이 없습니다.")
        comment.content = updated_comment.content
        comment.author = updated_comment.author
        session.add(comment)
        session.commit()
        session.refresh(comment)
    return comment


@router.patch("/comments/{comment_id}")
def patch_comment(comment_id: int, updated_fields: CommentUpdate):
    with Session(engine) as session:
        comment = session.get(Comment, comment_id)
        if not comment:
            raise HTTPException(status_code=404, detail=f"{comment_id}번 댓글이 없습니다.")
        update_data = updated_fields.model_dump(exclude_unset=True)
        for key, value in update_data.items():
            setattr(comment, key, value)
        session.add(comment)
        session.commit()
        session.refresh(comment)
    return comment


@router.delete("/comments/{comment_id}")
def delete_comment(comment_id: int):
    with Session(engine) as session:
        comment = session.get(Comment, comment_id)
        if not comment:
            raise HTTPException(status_code=404, detail=f"{comment_id}번 댓글이 없습니다.")
        session.delete(comment)
        session.commit()
    return {"message": f"{comment_id}번 댓글이 삭제되었습니다."}

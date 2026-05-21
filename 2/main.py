from pydantic import BaseModel
from fastapi import FastAPI
from typing import Optional

from ollama import chat
from ollama import ChatResponse

app = FastAPI()

class Post(BaseModel):
    id: int
    title: str
    content: str
    author: str
    summary: Optional[str] = None

class PostUpdate(BaseModel):
    title: Optional[str] = None
    content: Optional[str] = None
    author: Optional[str] = None

class Comment(BaseModel):
    id: int
    content: str
    author: str

class CommentUpdate(BaseModel):
    content: Optional[str] = None
    author: Optional[str] = None

posts = list()
comments = list()

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
    
    posts.append(post)
    return post

@app.get("/posts/")
def get_posts():
    return posts 

@app.put("/posts/{post_id}")
def update_post(post_id: int, updated_post: Post):
    for post in posts:
        if post.id == post_id:
            post.title = updated_post.title
            post.content = updated_post.content
            post.author = updated_post.author
            return post
    return {"message": f"{post_id}번 게시물이 없습니다."}

@app.patch("/posts/{post_id}")
def patch_post(post_id: int, updated_fields: PostUpdate):
    for post in posts:
        if post.id == post_id:
            update_data = updated_fields.dict(exclude_unset=True)

            for key, value in update_data.items():
                setattr(post, key, value)
            return post
    return {"message": f"{post_id}번 게시물이 없습니다."}

@app.delete("/posts/{post_id}")
def delete_post(post_id: int):
    global posts
    posts = [post for post in posts if post.id != post_id]
    return {"message": f"{post_id}번 게시물이 삭제되었습니다."}

@app.post("/comments/")
def create_comment(comment: Comment):
    comments.append(comment)
    return comment


@app.get("/comments/")
def get_comments():
    return comments

@app.delete("/comments/{comment_id}")
def delete_comment(comment_id: int):
    global comments
    comments = [comment for comment in comments if comment.id != comment_id]
    return {"message": f"{comment_id}번 댓글이 삭제되었습니다."}

@app.put("/comments/{comment_id}")
def update_comment(comment_id: int, updated_comment: Comment):
    for comment in comments:
        if comment.id == comment_id:
            comment.content = updated_comment.content
            comment.author = updated_comment.author
            return comment
    return {"message": f"{comment_id}번 댓글이 없습니다."}

@app.patch("/comments/{comment_id}")
def patch_comment(comment_id: int, updated_fields: CommentUpdate):
    for comment in comments:
        if comment.id == comment_id:
            update_data = updated_fields.dict(exclude_unset=True)

            for key, value in update_data.items():
                setattr(comment, key, value)
            return comment
    return {"message": f"{comment_id}번 댓글이 없습니다."}


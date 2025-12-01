from fastapi import HTTPException
from sqlalchemy.orm import Session
from models.post_model import (
    create_post_data,
    update_post_data,
    delete_post_data,
    Post
)
from models.comment_model import Comment


def create_post(db: Session, author_id:int, data):
    if not data.title or not data.content:
        raise HTTPException(400, "제목, 내용을 모두 작성해주세요")

    if len(data.title) > 26:
        raise HTTPException(400, "제목 최대 26자")

    new_post = create_post_data(db, author_id, data.title, data.content,  data.image)
    return {"message": "게시글 등록 완료", "post": new_post}


def get_posts(db: Session, page: int = 1, size: int = 10):
    offset = (page - 1) * size

    posts = db.query(Post).order_by(Post.created_at.desc()).offset(offset).limit(size).all()

    result = []
    for post in posts:
        comment_count = db.query(Comment).filter(Comment.post_id == post.id).count()

        result.append({
            "id": post.id,
            "title": post.title,
            "views": post.views,
            "likes": post.likes,
            "author_id" : post.author_id,
            "created_at": post.created_at,
            "comments_count": comment_count,
        })

    return {"page": page, "size": size, "posts": result}


def get_post_detail(db: Session, post_id: int):
    post = db.query(Post).filter(Post.id == post_id).first()

    if not post:
        raise HTTPException(404, "게시글을 찾을 수 없습니다")

    post.views += 1
    db.commit()
    db.refresh(post)

    return {
        "id": post.id,
        "title": post.title,
        "content": post.content,
        "image": post.image,
        "views": post.views,
        "likes": post.likes,
        "author_id": post.author_id,
        "created_at": post.created_at
    }


def update_post(db: Session, post_id: int, author_id:int, data):
    post = db.query(Post).filter(Post.id == post_id).first()

    if len(data.title) > 26:
        raise HTTPException(400, "제목 최대 26자")

    updated = update_post_data(db, post_id, data.title, data.content)
    if updated:
        return {"message": "게시글 수정 완료", "post": updated}

    raise HTTPException(404, "게시글을 찾을 수 없습니다")

    if post.author_id != author_id:
        raise HTTPException(403, "수정 권한이 없습니다.")


def delete_post(db: Session, post_id: int):
    if delete_post_data(db, post_id):
        return {"message": "게시글 삭제 완료"}

    raise HTTPException(404, "게시글을 찾을 수 없습니다")

    if post.author_id != author_id:
        raise HTTPException(403, "삭제 권한이 없습니다.")

def toggle_like(db: Session, post_id: int, current_user_id: int):
    post = db.query(Post).filter(Post.id == post_id).first()
    if not post:
        raise HTTPException(404, "게시글을 찾을 수 없습니다")

    if post.likes == 0:
        post.likes = 1
        msg = "좋아요 추가"
    else:
        post.likes = 0
        msg = "좋아요 취소"

    db.commit()
    return {"message": msg, "likes": post.likes}

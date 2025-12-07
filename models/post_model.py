from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.orm import Session, relationship
from datetime import datetime
from database import Base
from datetime import datetime

# DB 테이블 정의
class Post(Base):
    __tablename__ = "posts"

    id = Column(Integer, primary_key = True, index = True)
    author_id = Column(Integer, ForeignKey("users.id"))
    title = Column(String, nullable = False)
    content = Column(String, nullable = False)
    image = Column(String, nullable = True)
    created_at = Column(DateTime, default = datetime.now)
    views = Column(Integer, default = 0)
    likes = Column(Integer, default = 0)


def create_post_data(db:Session, author_id, title, content, image= None):

    new_post = Post(
        author_id = author_id,
        title = title,
        content = content,
        image = image
    )
    db.add(new_post)
    db.commit()
    db.refresh(new_post)
    return new_post

# 최신순 정렬
def get_post_data(db:Session, skip: int = 0, limit: int=10):
    return db.query(Post).order_by(Post.created_at.desc()).offset(skip).limit(limit).all()

def get_post_by_id(db:Session, pid:int):
    return db.query(Post).filter(Post.id == pid).first()

def update_post_data(db:Session, pid: int, title, content, image = None):
    post = get_post_by_id(db, pid)
    if post:
        post.title = title
        post.content = content
        if image is not None:
            post.image = image
        db.commit()
        db.refresh(post)
        return post
    return None


def delete_post_data(db:Session, pid: int):
    post = get_post_by_id(db, pid)
    if post:
        db.delete(post)
        db.commit()
        return True
    return False

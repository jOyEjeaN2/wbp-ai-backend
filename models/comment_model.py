from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.orm import Session, relationship
from datetime import datetime
from database import Base

# DB 테이블 정의
class Comment(Base):
    __tablename__ = "comments"

    id = Column(Integer, primary_key = True, index = True)
    post_id = Column(Integer, ForeignKey('posts.id'))
    author_id = Column(Integer, ForeignKey('users.id'))
    content = Column(String, nullable = False)
    created_at = Column(DateTime, default = datetime.now)

def create_comment(db: Session, post_id: int, author_id: int, content: str):
    new_comment = Comment(
        post_id = post_id,
        author_id = author_id,
        content = content
    )
    db.add(new_comment)
    db.commit()
    db.refresh(new_comment)
    return new_comment

def get_comments_by_post(db: Session, post_id: int):
    return db.query(Comment).filter(Comment.post_id == post_id).all()


def get_comment_by_id(db: Session, cid: int):
    return db.query(Comment).filter(Comment.id == cid).first()


def update_comment_data(db: Session, cid: int, content: str):
    comment = get_comment_by_id(db, cid)
    if comment:
        comment.content = content
        db.commit()
        db.refresh(comment)
        return comment
    return None


def delete_comment_data(db: Session, cid: int):
    comment = get_comment_by_id(db, cid)
    if comment:
        db.delete(comment)
        db.commit()
        return True
    return False

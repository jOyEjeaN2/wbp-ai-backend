from fastapi import APIRouter, Depends
from pydantic import BaseModel
from sqlalchemy.orm import Session
from database import get_db
from controllers.comment_controller import (
    add_comment,
    update_comment,
    delete_comment,
    get_comments
)

router = APIRouter(prefix="/comments", tags=["Comments"])


class CommentReq(BaseModel):
    content: str
    author_id : int


@router.post("/{post_id}")
def add_comment_route(post_id: int, body: CommentReq, db: Session = Depends(get_db)):
    return add_comment(db, post_id, body.author_id, body.content)


@router.put("/{comment_id}")
def update_comment_route(comment_id: int, body: CommentReq, db: Session = Depends(get_db)):
    return update_comment(db, comment_id, body.content)

@router.get("/{post_id}")
def get_comments_route(post_id: int, db: Session = Depends(get_db)):
    return get_comments(db, post_id)


@router.delete("/{comment_id}")
def delete_comment_route(comment_id: int, db: Session = Depends(get_db)):
    return delete_comment(db, comment_id)

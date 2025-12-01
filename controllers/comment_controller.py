from fastapi import HTTPException
from sqlalchemy.orm import Session
from models.comment_model import (
    create_comment,
    get_comments_by_post,
    update_comment_data,
    delete_comment_data
)


def add_comment(db: Session, post_id: int, author_id: int, content: str):
    if not content:
        raise HTTPException(400, "댓글을 입력해주세요")

    comment = create_comment(db, post_id, author_id, content)
    return {"message": "댓글 등록 완료", "comment": comment}


def update_comment(db: Session, comment_id: int, content: str):
    if not content:
        raise HTTPException(400, "댓글을 입력해주세요")

    updated = update_comment_data(db, comment_id, content)
    if updated:
        return {"message": "댓글 수정 완료", "comment": updated}

    raise HTTPException(404, "댓글을 찾을 수 없습니다")


def delete_comment(db: Session, comment_id: int):
    if delete_comment_data(db, comment_id):
        return {"message": "댓글 삭제 완료"}

    raise HTTPException(404, "댓글을 찾을 수 없습니다")


def get_comments(db: Session, post_id: int):
    return get_comments_by_post(db, post_id)


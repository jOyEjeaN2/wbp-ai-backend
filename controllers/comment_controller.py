from fastapi import HTTPException
from sqlalchemy.orm import Session
from models.comment_model import (
    create_comment,
    get_comments_by_post,
    update_comment_data,
    delete_comment_data,
    get_comment_by_id
)

from models.user_model import User

def add_comment(db: Session, post_id: int, author_id: int, content: str):
    if not content:
        raise HTTPException(400, "댓글을 입력해주세요")

    comment = create_comment(db, post_id, author_id, content)

    # ORM 객체를 딕셔너리로 변환
    comment_dict = comment.__dict__.copy()
    comment_dict.pop('_sa_instance_state', None)

    author = db.query(User).filter(User.id == author_id).first()
    comment_dict["author_nickname"] = author.nickname if author else "알 수 없음"
    return {"message": "댓글 등록 완료", "comment": comment}


def update_comment(db: Session, comment_id: int, author_id: int, content: str):
    comment = get_comment_by_id(db, comment_id)
    if not comment:
        raise HTTPException(404, "댓글을 찾을 수 없습니다")

    if comment.author_id != author_id:
        raise HTTPException(403, "수정 권한이 없습니다.")

    if not content:
        raise HTTPException(400, "댓글을 입력해주세요")

    updated = update_comment_data(db, comment_id, content)
    if updated:
        return {"message": "댓글 수정 완료", "comment": updated}

    raise HTTPException(404, "댓글을 찾을 수 없습니다")


def delete_comment(db: Session, comment_id: int, author_id: int):
    comment = get_comment_by_id(db, comment_id)
    if not comment:
        raise HTTPException(404, "댓글을 찾을 수 없습니다")

    if delete_comment_data(db, comment_id):
        return {"message": "댓글 삭제 완료"}

    if comment.author_id != author_id:
        raise HTTPException(403, "삭제 권한이 없습니다.")

    raise HTTPException(404, "댓글을 찾을 수 없습니다")


def get_comments(db: Session, post_id: int):
    comments = get_comments_by_post(db, post_id)

    result = []
    for comment in comments:
        comment_dict = comment.__dict__.copy()
        comment_dict.pop('_sa_instance_state', None)

        author = db.query(User).filter(User.id == comment.author_id).first()
        comment_dict["author_nickname"] = author.nickname if author else "알 수 없음"
        result.append(comment_dict)

    return result


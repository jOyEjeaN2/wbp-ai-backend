from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from database import get_db
from pydantic import BaseModel
from controllers.post_controller import (
    get_posts,
    create_post,
    get_post_detail,
    update_post,
    delete_post,
    toggle_like
)
from dependencies.auth_dep import get_current_user_id

router = APIRouter(prefix="/posts", tags=["Posts"])



class PostCreate(BaseModel):
    title: str
    content: str
    image : str | None = None

class PostUpdate(BaseModel):
    title: str
    content: str


# 게시글 목록 조회
@router.get("")
def get_posts_route(page:int=1, size: int=10, db:Session = Depends(get_db)):
    return get_posts(db, page, size)


# 게시글 생성
@router.post("")
def create_post_route(body: PostCreate, db:Session = Depends(get_db), current_user_id: int=Depends(get_current_user_id)):
    return create_post(db, current_user_id, body)


# 게시글 상세 조회
@router.get("/{post_id}")
def get_post_detail_route(post_id: int, db:Session = Depends(get_db)):
    return get_post_detail(db, post_id)


# 게시글 수정
@router.put("/{post_id}")
def update_post_route(post_id: int, body: PostUpdate, db:Session = Depends(get_db), current_user_id: int = Depends(get_current_user_id)):
    return update_post(db, post_id, current_user_id, body)


# 게시글 삭제
@router.delete("/{post_id}")
def delete_post_route(post_id: int, db:Session = Depends(get_db), current_user_id: int = Depends(get_current_user_id)):
    return delete_post(db, post_id, current_user_id)


# 좋아요 토글
@router.post("/{post_id}/like")
def toggle_like_route(post_id: int, db:Session = Depends(get_db), current_user_id: int = Depends(get_current_user_id)):
    return toggle_like(db, post_id, current_user_id)

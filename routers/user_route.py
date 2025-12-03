from fastapi import APIRouter, Body, Depends, UploadFile, File, Form
from sqlalchemy.orm import Session
from database import get_db
from pydantic import BaseModel
from controllers.user_controller import (
    update_profile,
    update_password,
    logout,
    delete_user,
)
from dependencies.auth_dep import get_current_user_id
from typing import Optional
router = APIRouter(prefix="/users", tags=["Users"])

class ProfileUpdate(BaseModel):
    nickname: str


class PasswordUpdate(BaseModel):
    password: str
    confirm_password: str

# 프로필 수정
@router.put("/{user_id}/profile")
def update_profile_route(
    user_id: int,
    nickname: str = Form(...),
    profile_image: Optional[UploadFile] = File(None),
    db: Session = Depends(get_db),
    current_user_id: int = Depends(get_current_user_id)
):
    return update_profile(db, user_id, current_user_id, nickname, profile_image)


# 비밀번호 수정
@router.put("/{user_id}/password")
def update_password_route(
        user_id: int,
        body: PasswordUpdate,
        db:Session = Depends(get_db),
        current_user_id: int = Depends(get_current_user_id)
):
    return update_password(db, user_id, current_user_id, body.password, body.confirm_password)


@router.post("/logout")
def logout_route():
    from controllers.user_controller import logout
    return logout()

# 회원탈퇴
@router.delete("/{user_id}")
def delete_user_route(user_id: int, db:Session = Depends(get_db), current_user_id: int = Depends(get_current_user_id)):
    return delete_user(db, user_id, current_user_id)


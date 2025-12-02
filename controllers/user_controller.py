from fastapi import HTTPException, UploadFile, File, Form
from sqlalchemy.orm import Session
from models.user_model import (
    User,
    get_user_by_id,
    update_user_nickname,
    delete_user_data,
)
import shutil
import os
import re
from typing import Optional

# 이미지 저장 경로 설정 (없으면 자동 생성)
UPLOAD_DIR = "static/uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)


def update_profile(
        db: Session,
        user_id: int,
        current_user_id: int,
        nickname: str = Form(...),
        profile_image: Optional[UploadFile] = File(None)
):

    if user_id != current_user_id:
        raise HTTPException(403, "수정 권한이 없습니다.")

    if not nickname:
        raise HTTPException(400, "닉네임을 입력해주세요")

    if " " in nickname:
        raise HTTPException(400, "띄어쓰기를 없애주세요")

    if len(nickname) > 10:
        raise HTTPException(400, "닉네임은 최대 10자까지")

    existing_user = db.query(User).filter(User.nickname == nickname).first()
    if existing_user and existing_user.id != user_id:
        raise HTTPException(400, "중복된 닉네임입니다.")

    user = get_user_by_id(db, user_id)
    if not user:
        raise HTTPException(404, "유저를 찾을 수 없습니다.")


    image_url = user.profile_image


    if profile_image and hasattr(profile_image, 'filename') and profile_image.filename:
        # 파일 저장
        filename = f"{user_id}_{profile_image.filename}"
        file_path = os.path.join(UPLOAD_DIR, filename)

        with open(file_path, "wb") as buffer:
            shutil.copyfileobj(profile_image.file, buffer)

        # 웹 URL 변환
        image_url = f"/{UPLOAD_DIR}/{filename}".replace("\\", "/")

    user.nickname = nickname
    user.profile_image = image_url

    db.commit()
    db.refresh(user)

    return {
        "message": "수정완료",
        "updated_nickname": user.nickname,
        "updated_image": user.profile_image
    }


def update_password(db: Session, user_id: int, current_user_id: int, password: str, password_confirm: str):
    from models.user_model import update_user_password

    if int(user_id) != int(current_user_id):
        raise HTTPException(403, "수정 권한이 없습니다.")

    if not password or not password_confirm:
        raise HTTPException(400, "비밀번호를 입력해주세요")

    if password != password_confirm:
        raise HTTPException(400, "비밀번호가 다릅니다.")

    pattern = r"^(?=.*[A-Z])(?=.*[a-z])(?=.*\d)(?=.*\W).{8,20}$"
    if not re.match(pattern, password):
        raise HTTPException(400, "비밀번호 형식을 확인해주세요")

    from models.user_model import update_user_password
    updated = update_user_password(db, user_id, password)

    if updated:
        return {"message": "수정완료"}

    raise HTTPException(404, "유저를 찾을 수 없습니다.")


def logout():
    return {"message": "로그아웃 완료"}


def delete_user(db: Session, user_id: int, current_user_id: int):
    if int(user_id) != int(current_user_id):
        raise HTTPException(403, "삭제 권한이 없습니다.")

    if delete_user_data(db, user_id):
        return {"message": "회원탈퇴 완료"}

    raise HTTPException(404, "유저를 찾을 수 없습니다.")
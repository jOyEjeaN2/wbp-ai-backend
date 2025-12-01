from fastapi import HTTPException
from sqlalchemy.orm import Session
import re
from models.user_model import (
    User,
    get_user_by_id,
    update_user_nickname,
    update_user_password,
    delete_user_data,
)


def update_profile(db: Session, user_id: int, current_user_id: int,  nickname: str):
    print(f"👉 요청한 ID: {user_id} (타입: {type(user_id)})")
    print(f"👉 로그인 ID: {current_user_id} (타입: {type(current_user_id)})")
    print(f"👉 일치 여부: {user_id == current_user_id}")

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

    updated = update_user_nickname(db, user_id, nickname)
    if updated:
        return {"message": "수정완료", "updated_nickname": updated.nickname}

    raise HTTPException(404, "유저를 찾을 수 없습니다.")


def update_password(db:Session, user_id: int, current_user_id: int, password: str, password_confirm: str):
    if user_id != current_user_id:
        raise HTTPException(403, "수정 권한이 없습니다.")

    if not password or not password_confirm:
        raise HTTPException(400, "비밀번호를 입력해주세요")

    if password != password_confirm:
        raise HTTPException(400, "비밀번호가 다릅니다.")

    pattern = r"^(?=.*[A-Z])(?=.*[a-z])(?=.*\d)(?=.*\W).{8,20}$"
    if not re.match(pattern, password):
        raise HTTPException(400, "비밀번호 형식을 확인해주세요")

    updated = update_user_password(db, user_id, password)
    if updated:
        return {"message": "수정완료"}

    raise HTTPException(404, "유저를 찾을 수 없습니다.")


def logout():
    return {"message": "로그아웃 완료"}


def delete_user(db:Session, user_id: int, current_user_id: int):
    if user_id != current_user_id:
        raise HTTPException(403, "수정 권한이 없습니다.")

    if delete_user_data(db, user_id):
        return {"message": "회원탈퇴 완료"}

    raise HTTPException(404, "유저를 찾을 수 없습니다.")

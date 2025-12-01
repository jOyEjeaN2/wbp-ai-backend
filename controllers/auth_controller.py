from fastapi import HTTPException
from sqlalchemy.orm import Session
import re

from models.user_model import (
    create_user,
    User,
    add_login_session,
    remove_login_session,
    is_logged_in
)


def signup(db:Session, email: str, password: str, password_confirm: str, nickname: str, profile_image: str = None):

    if not email:
        raise HTTPException(400, "이메일을 입력해주세요")

    email_format = r"^[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}$"
    if not re.match(email_format, email):
        raise HTTPException(400, "올바른 이메일 형식입니다.")

    if db.query(User).filter(User.email == email).first():
        raise HTTPException(400, "중복된 이메일입니다.")

    if not password:
        raise HTTPException(400, "비밀번호를 입력해주세요")

    pw_rule = r"^(?=.*[A-Z])(?=.*[a-z])(?=.*\d)(?=.*\W).{8,20}$"
    if not re.match(pw_rule, password):
        raise HTTPException(400, "비밀번호 형식을 확인해주세요")

    if password != password_confirm:
        raise HTTPException(400, "비밀번호가 다릅니다.")

    if not nickname or " " in nickname or len(nickname) > 10:
        raise HTTPException(400, "닉네임 형식을 확인해주세요")

    new_user = create_user(db, email, password, nickname, profile_image)

    return {"message": "회원가입 완료", "user": new_user.id}


def login(db: Session, email: str, password: str):
    if not email:
        raise HTTPException(400, "이메일을 입력해주세요")

    user = db.query(User).filter(User.email == email).first()

    print(f"로그인 시도 이메일: {email}")
    print(f"DB에서 찾은 유저: {user}")

    if not user or not user.verify_password(password):
        raise HTTPException(400, "아이디 또는 비밀번호를 확인해주세요")

    add_login_session(user.id)

    return {"message": "로그인 성공", "user_id": user.id}


def logout(user_id: int):
    if not is_logged_in():
        raise HTTPException(400, "이미 로그아웃 상태입니다.")

    remove_login_session(user_id)
    return {"message" : "로그아웃 성공"}

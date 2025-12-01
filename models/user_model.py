from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import Session
from database import Base
from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


# DB 테이블 정의
class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index = True)
    email = Column(String, unique=True, index = True, nullable = False)
    password = Column(String, nullable = False)
    nickname = Column(String, unique=True, nullable = False)
    profile_image = Column(String, nullable = False)

    def verify_password(self, plain_password):
        return pwd_context.verify(plain_password, self.password)

    @staticmethod
    def get_password_hash(password):
        return pwd_context.hash(password)



def create_user(db: Session, email, password, nickname, profile_image=None):
    hashed_password = User.get_password_hash(password)

    new_user = {
        "email": email,
        "password": hashed_password,
        "nickname": nickname,
        "profile_image": profile_image
    }
    db.add(new_user)
    db.commit()
    db.refresh(new_user)


def get_user_by_email(db: Session, email: str):
    return db.query(User).filter(User.email == email).first()


def get_user_by_id(db: Session, uid: int):
    return db.query(User).filter(User.id == uid).first()


def update_user_nickname(db: Session, uid: int, new_nickname: str):
    user = get_user_by_id(db, uid)
    if user:
        user["nickname"] = new_nickname
        db.commit()
        db.refresh(user)
        return user
    return None


def update_user_password(db: Session, uid: int, new_password: str):
    user = get_user_by_id(db, uid)
    if user:
        user["password"] = User.get_password_hash(new_password)
        db.commit()
        db.refresh(user)
        return user
    return None


def delete_user_data(db:Session, uid: int):
    user = get_user_by_id(db, uid)
    if user:
        db.delete(user)
        db.commit()
        remove_login_session(uid)
        return True
    return False



# 로그인 세션 관리
# 임시 로그인 세션
active_sessions: set[int] = set()

def add_login_session(uid: int):
    active_sessions.add(uid)
    return True


def remove_login_session(uid: int):
    if uid in active_sessions:
        active_sessions.remove(uid)
        return True
    return False


def is_logged_in(uid: int):
    return uid in active_sessions

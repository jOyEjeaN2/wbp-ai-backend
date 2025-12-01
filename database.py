from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, DeclarativeBase

# 1. SQLite 데이터베이스 파일 경로 (프로젝트 폴더에 'wbp_db.db'라는 파일로 저장됨)
SQLALCHEMY_DATABASE_URL = "sqlite:///./wbp_db.db"

# 2. 엔진 생성 (SQLite 사용 시 check_same_thread=False 필수)
engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)

# 3. 세션 생성기 (데이터베이스와 대화하는 도구)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# 4. 모델들이 상속받을 기본 클래스
class Base(DeclarativeBase):
    pass

# 5. DB 세션을 가져오는 의존성 함수 (라우터에서 사용)
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
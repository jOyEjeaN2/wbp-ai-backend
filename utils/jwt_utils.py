from datetime import datetime, timedelta
from jose import jwt, JWTError
from fastapi import HTTPException

SECRETE_KEY = "my_super_secrete_key_change_this"
ALGORITHMS = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 60 * 24

def create_access_token(data: dict):
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})

    encoded_jwt = jwt.encode(to_encode, SECRETE_KEY, algorithm=ALGORITHMS)
    return encoded_jwt

def verify_token(token: str):
    try:
        payload = jwt.decode(token, SECRETE_KEY, algorithms=[ALGORITHMS])
        user_id: int = payload.get("sub")
        if user_id is None:
            raise HTTPException(status_code=401, detail="유효하지 않은 토큰입니다.")
        return int(user_id)
    except JWTError:
        raise HTTPException(status_code=401, detail = "로그인 후 이용해 주세요.")
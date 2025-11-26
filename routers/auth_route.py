from fastapi import APIRouter
from pydantic import BaseModel
from controllers.auth_controller import signup, login, logout

router = APIRouter(prefix="/auth", tags=["Auth"])


class SignupReq(BaseModel):
    email: str
    password: str
    password_confirm: str
    nickname: str
    profile_image: str | None = None


class LoginReq(BaseModel):
    email: str
    password: str


class LogoutReq(BaseModel):
    user_id: int


@router.post("/signup")
def signup_route(body: SignupReq):
    return signup(body.email, body.password, body.password_confirm, body.nickname, body.profile_image)


@router.post("/login")
def login_route(body: LoginReq):
    return login(body.email, body.password)


@router.post("/logout")
def logout_route(body: LogoutReq):
    return logout(body.user_id)

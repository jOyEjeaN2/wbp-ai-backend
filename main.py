from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from database import engine, Base
from models import user_model, post_model, comment_model

from routers.auth_route import router as auth_router
from routers.user_route import router as user_router
from routers.post_route import router as post_router
from routers.comment_route import router as comment_router
from routers.ai_route import router as ai_router

from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse

Base.metadata.create_all(bind = engine)

app = FastAPI(
    title="Community API",
    description="커뮤니티 백엔드 기능 테스트용 API",
    version="1.0.0"
)

origins = [
    "http://127.0.0.1:5500",
    "http://localhost:5500",
    "http://172.30.1.93:5500"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.mount("/static", StaticFiles(directory="static"), name="static")

app.include_router(auth_router)
app.include_router(user_router)
app.include_router(post_router)
app.include_router(comment_router)
app.include_router(ai_router)

@app.get("/")
async def read_index():
    return {"message": "Gaver API is running"}

## [FastAPI 커뮤니티 백엔드]
### FastAPI를 기반으로 JWT 인증, SQLite 데이터베이스 연동, AI 톤 변환 기능을 구현한 커뮤니티 백엔드 프로젝트


### [구조] 

```
project/
│
├─ main.py                 
├─ database.py              # 데이터베이스 연결 설정 (Engine, Session, Base)
│
├─ models/                  # 데이터베이스 스키마 정의 
│  ├─ user_model.py         # 사용자 모델 (User)
│  ├─ post_model.py         # 게시글 모델 (Post)
│  ├─ comment_model.py      # 댓글 모델 (Comment)
│  └─ ai_model.py           # AI 요청/응답 모델 (Pydantic)
│
├─ controllers/             # 비즈니스 로직 처리 (DB CRUD)
│  ├─ auth_controller.py    # 로그인/회원가입 
│  ├─ user_controller.py    # 회원 정보 수정/삭제 
│  ├─ post_controller.py    # 게시글 CRUD 
│  ├─ comment_controller.py # 댓글 CRUD 
│  └─ ai_controller.py      # AI 톤 변환 
│
├─ routers/                 # URL 경로
│  ├─ auth_route.py         # /auth (인증 관련 API)
│  ├─ user_route.py         # /users (회원 관련 API)
│  ├─ post_route.py         # /posts (게시글 관련 API)
│  ├─ comment_route.py      # /comments (댓글 관련 API)
│  └─ ai_route.py           # /ai_tone (AI 관련 API)
│
├─ utils/                   # 유틸리티 함수
│  └─ jwt_utils.py          # JWT 토큰 생성 및 검증 함수
│
└─ dependencies/            # 의존성 주입 (Dependency Injection)
   └─ auth_dep.py           # 인증 검사 미들웨어 (문지기 역할)
```


### 실행 
```
uvicorn main:app --reload  
http://localhost:8000/docs 
```

<br/>

## [AI] 게시글 톤 변환
사용자가 원하는 문체(Tone)를 입력하면, 게시글의 내용을 해당 스타일에 맞게 자연스럽게 변환해주는 AI 기능입니다.

### 지원 예시
다양한 말투와 사투리 변환을 지원합니다.

| 톤(Tone) | 변환 예시 |
| :--- | :--- |
| **사극** | "점심은 드셨사옵니까?" |
| **중2병** | "크크크... 내 안의 흑염룡이 날뛰는군..." |
| **전라도 사투리** | "아따, 밥은 먹었능가?" |
| **유치원생** | "선생님~ 저 배고파요!" |

### 🤖 사용 모델
- **Model:** `ollama-gemma3:4b` (On-device LLM)
- **Engine:** Ollama

  
## [API Routes 요약]
### 1. Auth (회원가입 / 로그인)
| Method | Endpoint       | Description |
| ------ | -------------- | ----------- |
| POST   | `/auth/signup` | 회원가입        |
| POST   | `/auth/login`  | 로그인         |


### 2. Users (프로필 / 비번 / 탈퇴)
| Method | Endpoint                    | Description |
| ------ | --------------------------- | ----------- |
| PUT    | `/users/{user_id}/profile`  | 닉네임 수정      |
| PUT    | `/users/{user_id}/password` | 비밀번호 수정     |
| POST   | `/users/logout`             | 로그아웃        |
| DELETE | `/users/{user_id}`          | 회원탈퇴        |

### 3. Posts (게시글)
| Method | Endpoint                | Description        |
| ------ | ----------------------- | ------------------ |
| GET    | `/posts`                | 게시글 목록 조회 (페이징 가능) |
| POST   | `/posts`                | 게시글 생성             |
| GET    | `/posts/{post_id}`      | 게시글 상세 조회          |
| PUT    | `/posts/{post_id}`      | 게시글 수정             |
| DELETE | `/posts/{post_id}`      | 게시글 삭제             |
| POST   | `/posts/{post_id}/like` | 좋아요 토글             |

### 4. Comments (댓글)
| Method | Endpoint                 | Description  |
| ------ | ------------------------ | ------------ |
| POST   | `/comments/{post_id}`    | 댓글 작성        |
| GET    | `/comments/{post_id}`    | 특정 게시글 댓글 조회 |
| PUT    | `/comments/{comment_id}` | 댓글 수정        |
| DELETE | `/comments/{comment_id}` | 댓글 삭제        |

### 5. 게시글 톤 변환 (AI)
| Method | Endpoint                 | Description  |
| ------ | ------------------------ | ------------ |
| POST   | `/ai_tone/convert`       | 게시글 톤 변환  |


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

## [AI] 강아지 커뮤니티 전용 글 톤/상담 변환

게시글 내용을 AI가 읽고, 사용자가 선택한 스타일에 맞게 문체를 바꿔주거나  
훈련사·수의사처럼 설명해주는 기능입니다.

### 지원 모드

- **톤 변환 모드 (재미용)**  
  글의 의미는 유지하면서 말투만 강아지스럽게/감성적으로 바꿔줍니다.

- **고민 상담 모드**  
  반려견 고민에 대해 훈련사·수의사처럼 차분하게 설명해주는 톤으로 변환합니다.  
  (※ 실제 전문가의 진단을 대신하지 않습니다.)

### 톤 프리셋 예시

| 구분 | 톤(Tone) | 설명 예시 |
| :--- | :--- | :--- |
| 재미 | **강아지 시점** | "오늘도 집사 따라 산책 다녀왔개! 간식 더 달라개!" |
| 재미 | **우리집 주인 자랑** | "우리 집사는 산책도 잘 해주고, 간식도 최고로 잘 챙겨줘요." |
| 재미 | **산책 일기** | "오늘은 강아지 공원까지 다녀왔어요. 새 친구도 만나고 냄새도 잔뜩 맡았어요." |
| 상담 | **훈련사 설명** | "이 행동은 분리불안의 신호일 수 있어요. 먼저 집을 비울 때 신호를 줄이는 연습부터 해보세요." |
| 상담 | **수의사처럼** | "최근에 식욕이 줄고 기운이 없다면, 위장 질환 가능성이 있어요. 증상이 지속되면 꼭 병원에 내원해주세요." |

사용자는 글을 작성한 뒤, 원하는 톤 프리셋을 선택하거나 직접 톤을 입력해  
버튼 한 번으로 변환 결과를 적용할 수 있습니다.


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


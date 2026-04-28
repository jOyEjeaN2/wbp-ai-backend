## [PawTalk Backend]
### 🐶 반려견 커뮤니티 백엔드 API 서버 (**FastAPI + AI (Ollama)** 기반)
**PawTalk**는 사용자가 작성한 글을 AI가 분석하여 강아지 시점의 말투나 전문가의 조언으로 변환해주는 기능을 제공합니다. </br>
외부 API 호출 없이 로컬에서 LLM을 구동하여 데이터 보안과 비용 효율성을 확보했습니다. 

### 🛠 Tech Stack
- **Framework & Language**
![Python](https://img.shields.io/badge/python-3.9+-3776AB?style=for-the-badge&logo=python&logoColor=white)
![FastAPI](https://img.shields.io/badge/FastAPI-005571?style=for-the-badge&logo=fastapi)

- **AI Engine** 
![Ollama](https://img.shields.io/badge/Ollama-Local_LLM-black?style=for-the-badge)

- **Database** 
![SQLite](https://img.shields.io/badge/sqlite-%2307405e.svg?style=for-the-badge&logo=sqlite&logoColor=white)
![SQLAlchemy](https://img.shields.io/badge/SQLAlchemy-D71F00?style=for-the-badge&logo=sqlalchemy&logoColor=white)


&nbsp; 

## 🏗 프로젝트 구조
유지보수와 확장성을 고려하여 Router - Controller - Model로 분리된 레이어드 아키텍처 채택
```
project/
├── main.py              # 앱 초기화 및 미들웨어 설정
├── database.py          # SQLAlchemy Engine 및 Session 설정
├── routers/             # API 엔드포인트 정의 (Interface Layer)
├── controllers/         # 비즈니스 로직 및 DB CRUD (Service Layer)
├── models/              # DB 테이블 스키마 및 Pydantic 모델
├── dependencies/        # JWT 인증 및 DB 세션 주입 (Security)
└── utils/               # 공통 유틸리티 (JWT 생성 등)
```

&nbsp;

## 🤖 AI 기능 : 반려견 커뮤니티 전용 글 톤/상담 변환

Ollama(Gemma3) 모델을 사용하여 텍스트의 페르소나를 변환

### 사용 모델
- **Model:** `ollama-gemma3:4b` (On-device LLM)
- **Engine:** Ollama

### 톤 변환 로직 
1. Prompt Enginering : 사용자가 선택한 모드에 맞춰 AI가 자연스러운 말투를 사용하도록 설계
2. 자체 서버 처리 : 로컬 서버에서 직접 LLM을 실행하여 네트워크 지연 시간을 최소화하고 개인정보 보호

### 지원 모드

- **톤 변환 모드 (재미용)**  
  글의 의미는 유지하면서 말투만 강아지스럽게/감성적으로 바꿈

- **고민 상담 모드**  
  반려견 고민에 대해 훈련사·수의사처럼 차분하게 설명해주는 톤으로 변환
  (※ 실제 전문가의 진단을 대신하지 않음.)

### 톤 프리셋 예시

| 구분 | 톤(Tone) | 설명 예시 |
| :--- | :--- | :--- |
| 재미 | **강아지 시점** | "오늘도 집사 따라 산책 다녀왔다! 간식 더 달라!" |
| 재미 | **우리집 주인 자랑** | "우리 집사는 산책도 잘 해주고, 간식도 최고로 잘 챙겨줘요." |
| 재미 | **산책 일기** | "오늘은 강아지 공원까지 다녀왔어요. 새 친구도 만나고 냄새도 잔뜩 맡았어요." |
| 상담 | **훈련사 설명** | "이 행동은 분리불안의 신호일 수 있어요. 먼저 집을 비울 때 신호를 줄이는 연습부터 해보세요." |
| 상담 | **수의사처럼** | "최근에 식욕이 줄고 기운이 없다면, 위장 질환 가능성이 있어요. 증상이 지속되면 꼭 병원에 내원해주세요." |

사용자는 글을 작성한 뒤, 원하는 톤 프리셋을 선택하거나 직접 톤을 입력해 버튼 한 번으로 변환 결과를 적용할 수 있음



&nbsp; 


## API Routes 요약
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


&nbsp; 

## 🚀 시작하기
**1. Ollama 설치 및 모델 다운로드**
```
ollama pull gemma3:4b
```
**2. 패키지 설치**
```
pip install -r requirements.txt
```
**3. 실행**
```
uvicorn main:app --reload  
http://localhost:8000/docs 
```

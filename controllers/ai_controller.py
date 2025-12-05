import requests
import json
from models.ai_model import ToneRequest, ToneResponse

OLLAMA_URL = "http://localhost:11434/api/generate"
MODEL_NAME = "gemma3:4b"

class AIController:
    @staticmethod
    def change_tone_logic(request: ToneRequest) -> ToneResponse:

        tone_examples = {
            "강아지 시점": """
                    [예시]
                    입력: 뭐해? -> 출력 : 주인 지금 뭐해? 나랑 놀아줘!
                    입력: 뭐먹어? -> 출력 : 주인,,,지금 뭐 먹어,,? 나도 줘! 
                    """,

            "우리집 주인 자랑(강아지 시점에서)": """
                    [예시]
                    입력: 오늘 간식을 먹었다. -> 출력: 우리 주인이 간식을 주더라고~
                    """,

            "훈련사 설명": """
                    [예시]
                    입력: 자꾸 짖어요 -> 출력: 이는 보호자 요구 행동 강화 패턴이 형성된 것으로 보이며, 자극 통제 훈련을 병행하면 개선됩니다.
                    """,

            "수의사처럼": """
                    [예시]
                    입력: 밥을 잘 안 먹어요 -> 출력: 식욕 저하는 스트레스, 위장 문제, 또는 급격한 환경 변화 때문일 가능성이 있습니다. 추가 증상을 관찰해보시면 좋겠습니다.
                    """,

            "산책 일기": """
                    [예시]
                    입력: 산책 갔다 왔어요 -> 출력: 오늘 산책 길의 바람은 유난히 부드러웠고, 우리 강아지는 풀 냄새를 맡으며 행복해했습니다.
                    """,

            "정보글 요약": """
                    [예시]
                    입력: 강아지가 자꾸 긁어요 -> 출력: • 피부 알레르기 가능성 있음 • 환경 변화 체크 필요 • 목욕 주기 점검 권장
                    """,

            "고민 상담": """
                    [예시]
                    입력: 강아지가 말을 안 들어요 -> 출력: 요즘 강아지가 이전보다 훈련에 반응하지 않아 많이 걱정돼요. 혹시 제가 뭔가 잘못하고 있는 걸까요?
                    """,

            "썰 푸는 톤": """
                    [예시]
                    입력: 강아지가 간식을 훔쳐 먹었어요 -> 출력: 우리 집 댕댕이, 잠깐 조용하다 싶더니 간식 창고를 털어놨더라고요. 진짜 도둑고양이도 울고 갈 포스임.
                    """,

            "첫 반려견": """
                    [예시]
                    입력: 어떻게 해야 하나요 -> 출력: 첫 강아지라 정말 모든 게 낯설고 어렵네요. 조언 부탁드려요.
                    """,

        }

        prompt = f"""
        
        역할: 당신은 '문체 변환 전문가'입니다. 
        지시: 입력된 문장의 의미를 유지하면서 '{request.tone}' 말투로 자연스럽게 바꿔주세요. 
        제약사항: 
            1. 부가적인 설명이나 인사말(예: "네, 알겠습니다.")은 절대 하지 마세요.
            2. 오직 변환된 문장만 출력하세요.
            3. 입력된 문장의 원래 의미는 유지하세요.
            4. 입력 문장에 한자나 영어, 외국어가 있으면 자연스러운 한국어로 의역하여 변환하세요. 
            5. 억지로 길게 늘리지 말고 간결하고 자연스럽게 표현하세요.
        
        {tone_examples} 
        
        입력 문장: {request.text}
        """

        payload = {
            "model" : MODEL_NAME,
            "prompt" : prompt,
            "stream": False,
            "temperature" : 0.8
        }

        try:
            response = requests.post(OLLAMA_URL, json=payload)
            response.raise_for_status()

            result_json = response.json()
            converted_text = result_json.get("response","").strip()

            if converted_text.startswith('"') and converted_text.endswith('"'):
                converted_text = converted_text[1:-1]

            return ToneResponse(
                original_text=request.text,
                converted_text=converted_text,
                tone_used=request.tone
            )
        except requests.exceptions.RequestException as e:
            print(f"Ollama 연결 에러: {e}")
            return ToneResponse(
                original_text=request.text,
                converted_text="AI 서버 연결에 실패했습니다.",
                tone_used="Error"
            )
import requests
import json
from models.ai_model import ToneRequest, ToneResponse

OLLAMA_URL = "http://localhost:11434/api/generate"
MODEL_NAME = "gemma3:4b"

class AIController:
    @staticmethod
    def change_tone_logic(request: ToneRequest) -> ToneResponse:
        examples = ""
        if "사극" in request.tone:
            examples="""
            [예시] 
            입력: 안녕하세요 -> 출력: 평안하신가 
            입력: 야, 너 뭐하냐? -> 출력: 이보게, 자네 지금 무엇을 하는 겐가?
            입력: 이거 진짜 맛있다. -> 출력: 이 맛이 실로 기가 막히구나.
            """
        elif "전라도 사투리" in request.tone:
            examples="""
            [예시]
            입력: 뭐하냐? -> 출력: 뭣허냐? 
            입력: 미치겠네 -> 출력: 미쳐블겄네
            입력: 난 이런거 못해 -> 출력: 난 이런거 모대
            입력: 이런! -> 출력: 오메!
            """


        prompt = f"""
        
        역할: 당신은 '문체 변환 전문가'입니다. 
        지시: 입력된 문장의 의미를 유지하면서 '{request.tone}' 말투로 자연스럽게 바꿔주세요. 
        제약사항: 
            1. 부가적인 설명이나 인사말(예: "네, 알겠습니다.")은 절대 하지 마세요.
            2. 오직 변환된 문장만 출력하세요.
            3. 입력된 문장의 원래 의미는 유지하세요.
            4. 입력 문장에 한자나 영어, 외국어가 있으면 자연스러운 한국어로 의역하여 변환하세요. 
            5. 억지로 길게 늘리지 말고 간결하고 자연스럽게 표현하세요.
        
        {examples} 
        
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
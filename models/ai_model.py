from pydantic import BaseModel

class ToneRequest(BaseModel):
    text: str
    tone: str

class ToneResponse(BaseModel):
    original_text : str
    converted_text : str
    tone_used: str
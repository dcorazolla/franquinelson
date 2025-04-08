from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from src.core.assistant import Assistant

router = APIRouter()

# instância do assistente
assistant = Assistant()

class ChatRequest(BaseModel):
    prompt: str

class ChatResponse(BaseModel):
    response: str

@router.post("/", response_model=ChatResponse)
def chat(request: ChatRequest):
    if not request.prompt.strip():
        raise HTTPException(status_code=400, detail="Prompt não pode ser vazio.")

    resposta = assistant.response(request.prompt)
    return ChatResponse(response=resposta)

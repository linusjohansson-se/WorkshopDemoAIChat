from typing import Optional
from application.llm_chat import send_message
from fastapi import APIRouter
import uuid
from infrastructure.llm import get_chat_llm

router = APIRouter(prefix="/chat", tags=["chat"])

@router.post("")
async def chat(msg: str, id: Optional[uuid.UUID] = None):
    answer = await send_message(msg, id)
    return {"answer": answer}
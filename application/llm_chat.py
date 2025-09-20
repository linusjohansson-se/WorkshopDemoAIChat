from typing import Dict, Optional
from infrastructure.llm import get_chat_llm
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables.history import RunnableWithMessageHistory
from langchain_core.chat_history import InMemoryChatMessageHistory
from langchain_core.chat_history import BaseChatMessageHistory

from collections import defaultdict
import uuid

_histories: Dict[str, InMemoryChatMessageHistory] = defaultdict(InMemoryChatMessageHistory)

def get_session_history(session_id: str) -> BaseChatMessageHistory:
    return _histories[session_id]

_llm = get_chat_llm()

_prompt = ChatPromptTemplate.from_messages([
    ("system", "You are a helpful assistant."),
    MessagesPlaceholder("history"),
    ("human", "{input}"),
])

_base_chain = _prompt | _llm | StrOutputParser()

_chain_with_history = RunnableWithMessageHistory(
    _base_chain,
    get_session_history=get_session_history,
    input_messages_key="input",
    history_messages_key="history",
)

async def send_message(msg: str, id: Optional[uuid.UUID] = None):

    if id is None:
        answer = await _base_chain.ainvoke({"input": msg})
        return answer

    cfg = {"configurable": {"session_id": str(id)}}

    answer = await _chain_with_history.ainvoke({"input": msg}, config=cfg)

    return answer


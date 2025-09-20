from typing import Dict, Optional
from infrastructure.llm import get_chat_llm
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.output_parsers import StrOutputParser
from langchain.agents import create_openai_tools_agent, AgentExecutor
from langchain_core.runnables.history import RunnableWithMessageHistory
from langchain_core.chat_history import InMemoryChatMessageHistory
from langchain_core.chat_history import BaseChatMessageHistory
from application.tools import TOOLS

from collections import defaultdict
import uuid

_histories: Dict[str, InMemoryChatMessageHistory] = defaultdict(InMemoryChatMessageHistory)

def get_session_history(session_id: str) -> BaseChatMessageHistory:
    return _histories[session_id]

_llm = get_chat_llm()

_system_message = (
    "You are a Michelin-star chef. "
    "Be practical. Use tools when they help (e.g., conversions, pantry checks)."
)

_prompt = ChatPromptTemplate.from_messages([
    ("system", _system_message),
    MessagesPlaceholder("history"),
    ("human", "{input}"),
    MessagesPlaceholder("agent_scratchpad"),
])

agent = create_openai_tools_agent(_llm, TOOLS, _prompt)
agent_exec = AgentExecutor(agent=agent, tools=TOOLS, verbose=False)


#_base_chain = _prompt | _llm | StrOutputParser()

_chain_with_history = RunnableWithMessageHistory(
    agent_exec,
    get_session_history=get_session_history,
    input_messages_key="input",
    history_messages_key="history",
)

_prompt_no_hist = ChatPromptTemplate.from_messages([
    ("system", _system_message),
    ("human", "{input}"),
    MessagesPlaceholder("agent_scratchpad"),
])

agent_nohist = create_openai_tools_agent(_llm, TOOLS, _prompt_no_hist)
agent_exec_nohist = AgentExecutor(agent=agent_nohist, tools=TOOLS, verbose=False)

#_chain_without_history = _prompt_no_hist | _llm | StrOutputParser()

async def send_message(msg: str, id: Optional[uuid.UUID] = None):

    if id is None:
        answer = await agent_exec_nohist.ainvoke({"input": msg})
        return answer

    cfg = {"configurable": {"session_id": str(id)}}

    answer = await _chain_with_history.ainvoke({"input": msg}, config=cfg)

    return answer


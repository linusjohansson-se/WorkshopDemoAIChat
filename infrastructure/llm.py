import os
from langchain_google_genai import ChatGoogleGenerativeAI

CHAT_LLM = None

def setup_llm():
    global CHAT_LLM

    provider = os.getenv("LLM_PROVIDER")
    model = os.getenv("LLM_MODEL")
    key = os.getenv("LLM_API_KEY")
    
    if provider is None or model is None:
        raise ValueError("Missing required env vars: LLM_PROVIDER and/or LLM_MODEL")

    if provider.lower() == "google":
        CHAT_LLM = ChatGoogleGenerativeAI(
            model=model,
            api_key=key
        )
    else:
        raise ValueError(f"Unsupported LLM_PROVIDER: {provider}")

    print(f"LLM initialized with provider={provider}, model={model}")
        

def get_chat_llm():
    global CHAT_LLM
    if CHAT_LLM is None:
        raise RuntimeError("LLM not initialized. Call setup_llm() first.")
    return CHAT_LLM
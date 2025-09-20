from langchain_google_genai import ChatGoogleGenerativeAI

def setup_llm(app):
    app.state.llm = ChatGoogleGenerativeAI()

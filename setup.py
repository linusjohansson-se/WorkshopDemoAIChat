from fastapi import FastAPI
from dotenv import load_dotenv
from application.endpoints.chat import router as chat_router
from infrastructure.llm import setup_llm

async def lifespan(app: FastAPI):
    # Startup logic
    print("Starting up...")
    
    # one-time setup
    setup_llm()

    yield
    # Shutdown logic
    print("Shutting down...")
    
def add_routers(app: FastAPI):
    #Include any API routers here
    app.include_router(chat_router)
    return app

def setup():
    load_dotenv()
    if __debug__:
        load_dotenv(".env")
    else:
        load_dotenv("prod.env")
    
    app = FastAPI(lifespan=lifespan)
    app = add_routers(app)
    return app
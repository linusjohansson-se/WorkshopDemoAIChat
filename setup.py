from fastapi import FastAPI
from dotenv import load_dotenv
from application.endpoints.chat import router as chat_router
import infrastructure.llm

load_dotenv()
if __debug__:
    load_dotenv(".env")
else:
    load_dotenv("prod.env")

async def lifespan(app: FastAPI):
    # Startup logic
    print("Starting up...")


    yield
    # Shutdown logic
    print("Shutting down...")
    
def add_routers(app: FastAPI):
    #Include any API routers here
    app.include_router(chat_router)
    return app

def setup():
    app = FastAPI(lifespan=lifespan)
    app = add_routers(app)
    return app
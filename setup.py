from fastapi import FastAPI
from dotenv import load_dotenv

async def lifespan(app: FastAPI):
    # one-time setup
    setup_llm(app, model="gpt-4o-mini", temperature=0.2)
    
    
    try:
        yield
    finally:
        # one-time teardown
        await dispose_db()

def add_routers(app: FastAPI):
    #Include any API routers here
    return app

def setup():
    load_dotenv()
    
    app = FastAPI(lifespan=lifespan)
    app = add_routers(app)
    return app
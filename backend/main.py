from fastapi import FastAPI
from starlette.middleware.sessions import SessionMiddleware

from backend.api.endpoints import router as api_router

app = FastAPI(title="SimpleFlow API", version="1.0.0")

app.add_middleware(SessionMiddleware, secret_key="your_secret_key_here")

app.include_router(api_router)
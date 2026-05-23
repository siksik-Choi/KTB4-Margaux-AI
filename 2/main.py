from sqlmodel import SQLModel, Field, Session, create_engine, select
from fastapi import FastAPI
from typing import Optional

from ollama import chat
from ollama import ChatResponse

from fastapi import FastAPI, Request
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse

from database import init_db
from router import router as api_router


app = FastAPI()


@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    return JSONResponse(status_code=422, content={
        "detail": exc.errors(),
        "body": getattr(exc, 'body', None),
    })


app.include_router(api_router)


@app.on_event("startup")
def on_startup():
    init_db()
    author: Optional[str] = None



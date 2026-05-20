from fastapi import FastAPI
from contextlib import asynccontextmanager
from app.db.db import engine, Base
from app.api import categories, books

@asynccontextmanager
async def lifespan(app: FastAPI):
    Base.metadata.create_all(bind=engine)
    yield

app = FastAPI(title="Book API", lifespan=lifespan)

@app.get("/health")
def health_check():
    return {"status": "ok"}

app.include_router(categories.router)
app.include_router(books.router)

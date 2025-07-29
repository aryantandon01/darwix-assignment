from fastapi import FastAPI
from app.routers import calls, analytics
from app.database import engine, Base

Base.metadata.create_all(bind=engine)  # Create tables on startup

app = FastAPI(title="Sales Call Analytics")

app.include_router(calls.router, prefix="/api/v1")
app.include_router(analytics.router, prefix="/api/v1")

@app.get("/")
async def root():
    return {"message": "Welcome to Darwix AI Assignment API"}

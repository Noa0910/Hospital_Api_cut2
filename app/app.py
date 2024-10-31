from fastapi import FastAPI
from app.routes import router

app = FastAPI(title="Hospital Management System")

app.include_router(router, prefix="/api")

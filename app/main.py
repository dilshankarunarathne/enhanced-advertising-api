from fastapi import FastAPI

from app.auth import auth

app = FastAPI()

app.include_router(auth.router)
app.include_router()

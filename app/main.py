from fastapi import FastAPI

from app.data_access import auth

app = FastAPI()

app.include_router(auth.router)

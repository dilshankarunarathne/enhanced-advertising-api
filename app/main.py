from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.auth import auth
from app.routers import image

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth.router)
app.include_router(image.router)

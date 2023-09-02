from fastapi import APIRouter
from fastapi.security import OAuth2PasswordBearer



router = APIRouter(
    prefix="/auth",
    tags=["auth"],
    responses={404: {"description": "Not found"}},
)

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="http://127.0.0.1:8000/auth/token")

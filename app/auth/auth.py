from fastapi import APIRouter, Form, HTTPException, status
from fastapi.security import OAuth2PasswordBearer

from app.auth.models.user_model import UserInDB
from app.security.hashing import get_password_hash

"""
    routers for authentication
"""

router = APIRouter(
    prefix="/auth",
    tags=["auth"],
    responses={404: {"description": "Not found"}},
)

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="http://127.0.0.1:8000/auth/token")


@router.post("/register")
async def register_user(
        username: str = Form(...),
        email: str = Form(...),
        password: str = Form(...),
        is_adviser: bool = Form(...),
):
    if user_exists():
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Username already exists",
        )
    hashed_password = get_password_hash(password)
    user = UserInDB(
        id=get_next_avail_id(),
        username=username,
        email=email,
        hashed_password=hashed_password,
        is_adviser=is_adviser,
    )
    fake_users_db[username] = user.model_dump()
    return user

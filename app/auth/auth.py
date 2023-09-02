from datetime import timedelta
from typing import Annotated

from fastapi import APIRouter, Form, HTTPException, status, Depends
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm

from app.auth.models.user_model import UserInDB
from app.auth.user_dao import user_exists, get_next_avail_id, add_new_user, get_user
from app.security.hashing import get_password_hash, create_access_token, ACCESS_TOKEN_EXPIRE_MINUTES, verify_password

"""
    routers for authentication
"""

router = APIRouter(
    prefix="/auth",
    tags=["auth"],
    responses={404: {"description": "Not found"}},
)

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="http://127.0.0.1:8000/auth/token")


def authenticate_user(fake_db, username: str, password: str):
    user = get_user(fake_db, username)
    if not user:
        return False
    if not verify_password(password, user.hashed_password):
        return False
    return user


@router.post("/register")
async def register_user(
        username: str = Form(...),
        email: str = Form(...),
        password: str = Form(...),
        is_adviser: bool = Form(...),
):
    if user_exists(username):
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
    add_new_user(user)
    return user


@router.post("/login")
async def login_for_access_token(
        form_data: Annotated[OAuth2PasswordRequestForm, Depends()]
):
    user = authenticate_user(
        fake_users_db, form_data.username, form_data.password
    )
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.username}, expires_delta=access_token_expires.seconds
    )
    return {"access_token": access_token, "token_type": "bearer"}

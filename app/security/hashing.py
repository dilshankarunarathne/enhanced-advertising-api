from datetime import datetime, timedelta
from jose import jwt, JWTError
ACCESS_TOKEN_EXPIRE_MINUTES = 30


def decode_token(token):
    pass  # TODO: implement this method


def hash_password(password: str):
    pass  # TODO: implement this method


def create_access_token(data: dict, expires_delta: int = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + timedelta(minutes=expires_delta)
    else:
        expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)  # changes were made here
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

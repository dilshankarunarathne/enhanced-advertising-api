from datetime import datetime, timedelta

from jose import jwt

SECRET_KEY = "3ac975a63c346504ccc4bad65505c619a2cc502b01c7a92e3288f4d3b0def92b"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30




def create_access_token(data: dict, expires_delta: int = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + timedelta(minutes=expires_delta)
    else:
        expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

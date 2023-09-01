from fastapi.security import OAuth2PasswordBearer

from app.data_access.model.user_model import UserInDB

fake_users_db = {
    "johndoe": {
        "username": "johndoe",
        "email": "johndoe@example.com",
        "hashed_password": "fakehashedsecret",
        "is_adviser": False,
    },
    "alice": {
        "username": "alice",
        "email": "alice@example.com",
        "hashed_password": "fakehashedsecret2",
        "is_adviser": True,
    },
}

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")
# replace "token" with /token endpoint, this is where a client should obtain a token from


def get_user(db, username: str):
    if username in db:
        user_dict = db[username]
        return UserInDB(**user_dict)


def fake_decode_token(token):
    user = get_user(fake_users_db, token)
    return user

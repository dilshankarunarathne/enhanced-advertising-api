from fastapi.security import OAuth2PasswordBearer

fake_users_db = {
    "johndoe": {
        "username": "johndoe",
        "full_name": "John Doe",
        "email": "johndoe@example.com",
        "hashed_password": "fakehashedsecret",
        "is_adviser": False,
    },
    "alice": {
        "username": "alice",
        "full_name": "Alice Wonderson",
        "email": "alice@example.com",
        "hashed_password": "fakehashedsecret2",
        "is_adviser": True,
    },
}

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")
# replace "token" with /token endpoint, this is where a client should obtain a token from

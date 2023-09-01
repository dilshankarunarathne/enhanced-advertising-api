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

# replace "token" with '/token' endpoint, this is where a client should obtain a token from.
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


# this method is used to get a user from the db
# method should be able to get a user from the db based on the username that is passed in
# if the user exists, the method should return the user, otherwise it should return None.
# here, we are mocking the db with a dictionary
def get_user(db, username: str):
    if username in db:
        user_dict = db[username]
        return UserInDB(**user_dict)


# this method is used to verify the token.
# method should be able to evaluate a token sent by a client and check in the db to see if
# an actual user exists with the username that is encoded in the token. If the user exists,
# the method should return the user, otherwise it should return None.
# here, we are mocking the token with just by the username
def fake_decode_token(token):
    user = get_user(fake_users_db, token)
    return user

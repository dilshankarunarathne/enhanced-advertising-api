from datetime import datetime, timedelta
from typing import Annotated

from fastapi import HTTPException, status, Depends, APIRouter
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from jose import jwt, JWTError
from passlib.context import CryptContext

from app.data_access.model.token_dao import TokenData
from app.data_access.model.user_model import UserInDB, User

# to get a string like this run:
# openssl rand -hex 32
# this is the secret key that will be used to sign the JWT token
SECRET_KEY = "3ac975a63c346504ccc4bad65505c619a2cc502b01c7a92e3288f4d3b0def92b"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

fake_users_db = {
    "johndoe": {
        "id": 1,
        "username": "johndoe",
        "email": "johndoe@example.com",
        "hashed_password": "fake-hashed-secret",
        "is_adviser": False,
    },
    "alice": {
        "id": 2,
        "username": "alice",
        "email": "alice@example.com",
        "hashed_password": "fake-hashed-secret-2",
        "is_adviser": True,
    },
}


def fake_hash_password(password: str):
    return "fake-hashed-" + password


router = APIRouter(
    prefix="/mockAuth",
    tags=["mockAuth"],
    responses={404: {"description": "Not found"}},
)

# replace "token" with '/token' endpoint, this is where a client should obtain a token from.
# this is the endpoint that the client will send the username and password to, and if they are valid,
# the client will receive a token in return.
# this token will be used to authenticate the client in future requests.
# the client will send the token in the Authorization header of the request.
# the token is a random string that is generated by the server and is unique to the user.
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="http://127.0.0.1:8000/mockAuth/token")

# this is used to hash the password
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


# this method is used to verify that the password that is passed in matches the hashed password that is passed in.
def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)


# this method is used to hash the password that is passed in.
def get_password_hash(password):
    return pwd_context.hash(password)


# this method is used to get a user from the db
# method should be able to get a user from the db based on the username that is passed in
# if the user exists, the method should return the user, otherwise it should return None.
# here, we are mocking the db with a dictionary
def get_user(db, username: str):
    if username in db:
        user_dict = db[username]
        return UserInDB(**user_dict)


# this method is used to authenticate a user.
# method should be able to get the username and password from the request body and check in the db to see if
# an actual user exists with the username and password that are passed in. If the user exists,
# the method should return the user, otherwise it should return None.
def authenticate_user(fake_db, username: str, password: str):
    user = get_user(fake_db, username)
    if not user:
        return False
    if not verify_password(password, user.hashed_password):
        return False
    return user


# this method is used to create a token. This method will be used by the server to create a token for a user.
# method should be able to get the username and password from the request body and check in the db to see if
# an actual user exists with the username and password that are passed in. If the user exists, the method should
# create a token for the user and return the token, otherwise it should return None. The token should be a random
# string that is generated by the server and is unique to the user.
def create_access_token(data: dict, expires_delta: int = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + timedelta(minutes=expires_delta)
    else:
        expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)  # changes were made here
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


# this method is used to verify the token.
# method should be able to evaluate a token sent by a client and check in the db to see if
# an actual user exists with the username that is encoded in the token. If the user exists,
# the method should return the user, otherwise it should return None.
# here, we are mocking the token with just by the username
def fake_decode_token(token):
    user = get_user(fake_users_db, token)
    return user


# this method is used to get the current user.
# method should be able to get the token from the request header and check in the db to see if
# an actual user exists with the username that is encoded in the token. If the user exists,
# the method should return the user, otherwise it should raise an exception.
# here, we are mocking the token with just by the username and the db with a dictionary
async def get_current_user(token: Annotated[str, Depends(oauth2_scheme)]):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
        token_data = TokenData(username=username)
    except JWTError:
        raise credentials_exception
    user = get_user(fake_users_db, username=token_data.username)
    if user is None:
        raise credentials_exception
    return user


# tested - working...! :)
# this method is used by the users to acquire a token (login).
# method should be able to get the username and password from the request body and check in the db to see if
# an actual user exists with the username and password that are passed in. If the user exists,
# the method should return the user, otherwise it should raise an exception.
@router.post("/token")
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
    # this is the token that will be returned to the client
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.username}, expires_delta=access_token_expires.seconds
    )
    return {"access_token": access_token, "token_type": "bearer"}


# endpoint for testing purposes
@router.get("/")
async def auth_root(current_user: Annotated[User, Depends(get_current_user)]):
    if current_user.is_adviser:
        return {"message": "Hello Adviser"}
    else:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid authentication credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )


#############################################################################################

class RegistrationForm():
    username: str
    email: str
    password: str
    is_adviser: bool


@router.post("/register")
async def register_user(
        form_data: Annotated[RegistrationForm, Depends()]
):
    if form_data.username in fake_users_db:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Username already exists",
            headers={"WWW-Authenticate": "Bearer"},
        )
    else:
        fake_users_db[form_data.username] = {
            "id": len(fake_users_db) + 1,
            "username": form_data.username,
            "email": form_data.email,
            "hashed_password": get_password_hash(form_data.password),
            "is_adviser": form_data.is_adviser,
        }
        return {"message": "User created successfully"}

from app.auth.dao.user_dao import UserDAO
from app.auth.models.user_model import User

user_dao = UserDAO(host="localhost", user="root", password="", database="enad")
user_dao.connect()


def add_new_user(user: User):
    user_dao.create_user(user)


def user_exists(username: str) -> bool:
    if get_user(username) is None:
        return False
    return True


def get_next_avail_id() -> int:
    user_dao.get_last_user_id()


def get_user(username: str):
    return user_dao.get_user_by_username(username)

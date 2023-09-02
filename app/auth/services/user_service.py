from app.auth.dao.user_dao import UserDAO
from app.auth.models.user_model import User

user_dao = UserDAO(host="localhost", user="root", password="", database="enad")
user_dao.connect()


def add_new_user(user: User):
    # TODO: implement this method
    pass


def user_exists(username: str) -> bool:
    if get_user(username) is None:
        return False


def get_next_avail_id() -> int:
    # TODO: implement this method
    pass


def get_user(username: str):
    return user_dao.get_user_by_username(username)
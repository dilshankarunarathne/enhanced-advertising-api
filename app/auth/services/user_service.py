user_dao = UserDAO(host="localhost", user="root", password="", database="enad")
user_dao.connect()


def add_new_user(user: User):
    # TODO: implement this method
    pass


def user_exists(username: str) -> bool:
    # TODO: implement this method
    pass


def get_next_avail_id() -> int:
    # TODO: implement this method
    pass


def get_user(username: str):
    return get_user_by_username(username)
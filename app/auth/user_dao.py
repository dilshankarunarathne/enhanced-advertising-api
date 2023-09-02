from app.auth.models.user_model import User, UserInDB

"""
    middleware for accessing the database and performing CRUD operations on the user table
"""


def add_new_user(user: User):
    # TODO: implement this method
    pass


def user_exists(username: str) -> bool:
    # TODO: implement this method
    pass


def get_next_avail_id() -> int:
    # TODO: implement this method
    pass


# 
def get_user(db, username: str):
    # TODO: implement this method
    pass

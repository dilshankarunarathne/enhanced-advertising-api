import mysql.connector
from mysql.connector import errorcode

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


def get_user(username: str):
    # TODO: implement this method
    # check if the user exists in the db and if so, construct and return a UserInDB object
    pass


class UserDAO:
    def __init__(self, host, user, password, database):
        self.host = host
        self.user = user
        self.password = password
        self.database = database
        self.cnx = None

    def connect(self):
        try:
            self.cnx = mysql.connector.connect(
                host=self.host,
                user=self.user,
                password=self.password,
                database=self.database
            )
        except mysql.connector.Error as err:
            if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
                print("Something is wrong with your user name or password")
            elif err.errno == errorcode.ER_BAD_DB_ERROR:
                print("Database does not exist")
            else:
                print(err)

    def disconnect(self):
        if self.cnx is not None:
            self.cnx.close()

    def create_user(self, user: User):
        cursor = self.cnx.cursor()
        add_user = ("INSERT INTO users "
                    "(id, username, email, is_adviser, hashed_password) "
                    "VALUES (%s, %s, %s, %s, %s)")
        data_user = (user.id, user.username, user.email, user.is_adviser, user.hashed_password)
        cursor.execute(add_user, data_user)
        self.cnx.commit()
        cursor.close()

    def get_user_by_id(self, user_id: int) -> UserInDB:
        cursor = self.cnx.cursor()
        query = ("SELECT id, username, email, is_adviser, hashed_password "
                 "FROM users "
                 "WHERE id = %s")
        cursor.execute(query, (user_id,))
        row = cursor.fetchone()
        cursor.close()
        if row is None:
            return None
        return UserInDB(**dict(zip(['id', 'username', 'email', 'is_adviser', 'hashed_password'], row)))

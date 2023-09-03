dao = UserDAO(host="localhost", user="root", password="", database="enad")
try:
    user_dao.connect()
except Exception as e:
    print("User DB connection error:", e)
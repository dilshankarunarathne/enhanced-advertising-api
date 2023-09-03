from app.auth.dao.enad_dao import EnAdDAO

dao = EnAdDAO(host="localhost", user="root", password="", database="enad")
try:
    dao.connect()
    print("User DB connection successful")
except Exception as e:
    print("User DB connection error:", e)

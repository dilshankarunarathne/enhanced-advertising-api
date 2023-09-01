from fastapi import FastAPI

from data_access import mock_user_dao

app = FastAPI()

app.include_router(mock_user_dao.router)

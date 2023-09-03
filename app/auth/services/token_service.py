from app.auth.services.database_service import dao


def add_token_to_blacklist(token: str):
    dao.blacklist_token(token)


def check_if_token_is_blacklisted(token: str) -> bool:
    dao.is_token_blacklisted(token)

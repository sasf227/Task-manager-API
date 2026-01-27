from db_dependency import db_dependency
from pass_hash import verify_password
from get_user_info import get_user


def authenticate_user(db: db_dependency, username:str, password:str):
    user = get_user(db, username)
    if not user:
        return False 
    elif not verify_password(password, user.password_hash):
        return False
    return user
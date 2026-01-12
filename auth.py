from db_dependency import db_dependency
from db import User
from pass_hash import verify_password
from get_user_info import get_user


def authenticate_user(username:str, password:str, db: db_dependency):
    user = get_user(username, db)
    if not user:
        return False 
    elif not verify_password(password, user.password_hash):
        return False
    return user
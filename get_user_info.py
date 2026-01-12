from db_dependency import db_dependency
from db import User


def get_user(username: str, db: db_dependency):
    user = db.query(User).filter_by(username=username).first()
    return user

from fastapi.security import OAuth2PasswordBearer
from db_dependency import db_dependency
from db import User
from typing import Annotated
from fastapi import Depends, HTTPException, status
import jwt
from jwt.exceptions import InvalidTokenError
from db import TokenData, User

SECRET_KEY = "79558f3b2c4d75eb04107d8981edb6fc717b68fb2914018e6a7f5a18b83d900efb1f4edaedb50787ce666a7d194393546f4cd7d9a88561b60d41c47ea0f281009c26df51edcd25153bc2c87c53e00e3f3a20f947288c21c435ce60db4ced99659d15277e6723fdfed4afd90ed2da4a09c92dcff2ec96aa5de1ccb0f2cccee2d79e08d8ab525fbbe303734b4152b3817e7657f95fb889e307ee7a9454d4a65cb"
ALGORITHM = "HS256"
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

def get_user(db: db_dependency, username: str):
    user = db.query(User).filter_by(username=username).first()
    return user


async def get_current_user(token: Annotated[str, Depends(oauth2_scheme)], db: db_dependency):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=ALGORITHM)
        username = payload.get("sub")
        if username is None:
            raise credentials_exception
        token_data = TokenData(username=username)
    except InvalidTokenError:
        raise credentials_exception
    user = get_user(db, username=token_data.username)
    if user is None:
        raise credentials_exception
    return user

async def get_current_active_user(
    current_user: Annotated[User, Depends(get_current_user)],
):
    if current_user.disabled:
        raise HTTPException(status_code=400, detail="Inactive user")
    return current_user
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
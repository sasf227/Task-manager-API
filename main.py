from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from typing import List, Annotated
import jwt
from db_dependency import create_tables, db_dependency
from db import User, Tasks, Token, TokenSchema, UserSchema
from datetime import timedelta
from get_user_info import get_current_active_user
from woW import MY
from pass_hash import get_password_hash
from tokens import create_access_token




create_tables()


app = FastAPI()
SECRET_KEY = "79558f3b2c4d75eb04107d8981edb6fc717b68fb2914018e6a7f5a18b83d900efb1f4edaedb50787ce666a7d194393546f4cd7d9a88561b60d41c47ea0f281009c26df51edcd25153bc2c87c53e00e3f3a20f947288c21c435ce60db4ced99659d15277e6723fdfed4afd90ed2da4a09c92dcff2ec96aa5de1ccb0f2cccee2d79e08d8ab525fbbe303734b4152b3817e7657f95fb889e307ee7a9454d4a65cb"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")







@app.get ("/")
async def read_root(username: str, password: str, db: db_dependency):
    return {"message": "Welcome to FastAPI!"}


@app.post("/sign_in")
async def sign_in(username:str, password:str, db: db_dependency):
    hash_password = get_password_hash(password)
    e = User(username=username, password_hash=hash_password)
    db.add(e)
    db.commit()

@app.post("/log_in")
async def log_in(username:str, password:str, db: db_dependency):
    res = db.query(User).filter_by(username=username, password_hash=password).first()
    return MY(db, username, password)

@app.post("/token", response_model=TokenSchema)
async def login_for_access_token(db: db_dependency, form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
):
        user = MY(db, form_data.username, form_data.password)
        if not user:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Incorrect username or password",
                headers={"WWW-Authenticate": "Bearer"}
            )
        access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
        access_token = create_access_token(
            data = {"sub": user.username}, expires_delta=access_token_expires
        )
        return Token(access_token=access_token, token_type="bearer")
        
        
@app.get("/users/me/", response_model=UserSchema)
async def read_user_me(
    current_user: Annotated[User, Depends(get_current_active_user)],
):
    return current_user

@app.get("/users/me/items/", response_model=UserSchema)
async def read_own_items(
    current_user: Annotated[User, Depends(get_current_active_user)],
):
    return [{"item_id": "Foo", "owner": current_user.username}]
        
if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
        

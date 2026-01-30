from fastapi import FastAPI, Depends, HTTPException, status, Request
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from typing import List, Annotated
import jwt
from requests import session
from db_dependency import create_tables, db_dependency
from db import User, Tasks, Token, TokenSchema, UserSchema
from datetime import timedelta
from get_user_info import get_current_active_user
from auth import authenticate_user
from pass_hash import get_password_hash
from tokens import create_access_token
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse


create_tables()


app = FastAPI()
app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")
SECRET_KEY = "79558f3b2c4d75eb04107d8981edb6fc717b68fb2914018e6a7f5a18b83d900efb1f4edaedb50787ce666a7d194393546f4cd7d9a88561b60d41c47ea0f281009c26df51edcd25153bc2c87c53e00e3f3a20f947288c21c435ce60db4ced99659d15277e6723fdfed4afd90ed2da4a09c92dcff2ec96aa5de1ccb0f2cccee2d79e08d8ab525fbbe303734b4152b3817e7657f95fb889e307ee7a9454d4a65cb"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")




    
@app.get("/home", response_class=HTMLResponse)
async def home(request: Request):
    return templates.TemplateResponse(request=request, name="home_page.html")


@app.get("/login", response_class=HTMLResponse)
async def login(request: Request):
    return templates.TemplateResponse(request=request, name="login.html")

@app.post("/sign_in")
async def sign_in(username:str, password:str, db: db_dependency):
    hash_password = get_password_hash(password)
    e = User(username=username, password_hash=hash_password)
    db.add(e)
    db.commit()

@app.post("/log_in")
async def log_in(username:str, password:str, db: db_dependency):
    res = db.query(User).filter_by(username=username, password_hash=password).first()
    return authenticate_user(db, username, password)

@app.post("/token", response_model=TokenSchema)
async def login_for_access_token(db: db_dependency, form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
):
        user = authenticate_user(db, form_data.username, form_data.password)
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

        return {
            "access_token": access_token,
            "token_type": "bearer"
        }, home(request=Request)
        
        


@app.get("/users/me/items/")
async def read_own_items(
    current_user: Annotated[User, Depends(get_current_active_user)],
):
    return [{"item_id": "Foo", "owner": current_user.username}]


@app.post("/handling", response_model=UserSchema)
async def handling(current_user: Annotated[User, Depends(get_current_active_user)]):
    return current_user

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
        

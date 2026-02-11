from fastapi import FastAPI, Depends, HTTPException, status, Request, Cookie
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from typing import List, Annotated
import jwt
from db_dependency import create_tables, db_dependency
from db import User, Tasks, TokenSchema, UserSchema
from datetime import timedelta
from get_user_info import get_current_active_user, get_user
from auth import authenticate_user
from pass_hash import get_password_hash
from tokens import create_access_token
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse, JSONResponse
from jwt.exceptions import InvalidTokenError
from schemas import UserCreate, Task, idT
from datetime import datetime


create_tables()


app = FastAPI()
app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")
SECRET_KEY = "79558f3b2c4d75eb04107d8981edb6fc717b68fb2914018e6a7f5a18b83d900efb1f4edaedb50787ce666a7d194393546f4cd7d9a88561b60d41c47ea0f281009c26df51edcd25153bc2c87c53e00e3f3a20f947288c21c435ce60db4ced99659d15277e6723fdfed4afd90ed2da4a09c92dcff2ec96aa5de1ccb0f2cccee2d79e08d8ab525fbbe303734b4152b3817e7657f95fb889e307ee7a9454d4a65cb"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")




    
@app.get("/home", response_class=HTMLResponse)
async def home(request: Request, db: db_dependency, access_token: str | None = Cookie(default=None)):
    if access_token:
        credentials_exception = HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )
        
        try:
            payload = jwt.decode(access_token, SECRET_KEY, algorithms=ALGORITHM)
            username = payload.get("sub")
            if username is None:
                raise credentials_exception
        except InvalidTokenError:
            raise credentials_exception
        user = get_user(db, username=username)
        if user is None:
            raise credentials_exception
        tasks = db.query(Tasks).filter_by(created_by=user.username).all()
        return templates.TemplateResponse(request=request, name="home_page.html", context={"username": user.username, "tasks": tasks})
    else:
        return "Logged out or sign in required"
    
@app.post("/logout")
async def logout():
    response = JSONResponse(content={"message": "Logged out"})
    response.delete_cookie(key="access_token")
    return response

@app.get("/login", response_class=HTMLResponse)
async def login(request: Request):
    return templates.TemplateResponse(request=request, name="login.html")

@app.get("/signup", response_class=HTMLResponse)
async def signup(request: Request):
    return templates.TemplateResponse(request=request, name="sign_up.html")


@app.post("/sign_up")
async def sign_up(user: UserCreate, db: db_dependency):
    hash_password = get_password_hash(user.password)
    e = User(username=user.username, password_hash=hash_password)
    db.add(e)
    db.commit()

@app.post("/token", response_model=TokenSchema)
async def login_for_access_token(form_data: Annotated[OAuth2PasswordRequestForm, Depends()], db: db_dependency,):
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

        response = JSONResponse (
            content={
                "access_token": access_token,
                "token_type": "bearer"
            }
        )
        
        response.set_cookie(
            key="access_token",
            value=access_token,
            httponly=True,
            secure=False,
            samesite="lax",
            max_age=1800
        )
        
        return response
        
        
@app.get("/newTask", response_class=HTMLResponse)
async def new_task(request: Request):
    return templates.TemplateResponse(request=request, name="newTask.html")

@app.post("/newTask_create")
async def new_task_create(db: db_dependency, task: Task, access_token: str | None = Cookie(default=None)):
    if access_token:
        credentials_exception = HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )
        
        try:
            payload = jwt.decode(access_token, SECRET_KEY, algorithms=ALGORITHM)
            username = payload.get("sub")
            if username is None:
                raise credentials_exception
        except InvalidTokenError:
            raise credentials_exception
        user = get_user(db, username=username)
        if user is None:
            raise credentials_exception
        task = Tasks(
            username_task=user.username,
            title=task.title,
            description=task.description,
            created_at=datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            created_by=user.username,
            time=task.time,
            date=task.date,
            status=["0%", "incomplete"],
            UT=task.underTasks
        )
        db.add(task)
        db.commit()
    else:
        return "Logged out or sign in required"
    

@app.get("/taskDetails/{title}", response_class=HTMLResponse)
async def taskDetails(title: str, request: Request, db: db_dependency):
    taskDetails = db.query(Tasks).filter_by(title=title).first()
    return templates.TemplateResponse(request=request, name="taskDetails.html", context={"taskDetails": taskDetails})
    
@app.post("/deleteTask")
async def deleteTask(idT: idT, db: db_dependency, access_token: str | None = Cookie(default=None)):
    if access_token:
        credentials_exception = HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )
        
        try:
            payload = jwt.decode(access_token, SECRET_KEY, algorithms=ALGORITHM)
            username = payload.get("sub")
            if username is None:
                raise credentials_exception
        except InvalidTokenError:
            raise credentials_exception
        user = get_user(db, username=username)
        if user is None:
            raise credentials_exception
        task = db.query(Tasks).filter_by(id=idT).first()
        db.delete(task)
        db.commit()
    else:
        return "Logged out or sign in required"

@app.get("/users/me/items/")
async def read_own_items(
    current_user: Annotated[User, Depends(get_current_active_user)],
):
    return [{"item_id": "Foo", "owner": current_user.username}]




if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
        

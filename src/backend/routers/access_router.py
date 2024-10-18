from typing import Annotated
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi import Request, APIRouter, HTTPException, Depends, Form, status
from datetime import timedelta, datetime, timezone

from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from passlib.context import CryptContext
from jose import jwt

from frontend.templates.templates_router import templates
from backend.database.database_conn import engine, SessionLocal
from backend.base_models.user_base_model import UserCreate
from backend.base_models.token_base_model import Token
from backend.database.models import user_db_model
from backend.database.models.user_db_model import Users

from sqlalchemy.orm import Session

# jwt preferences
SECRET = 'my-secret-key'
ALGORITHM = 'HS256'
TOKEN_MINS_EXPIRATION = 30

pswd_context = CryptContext(schemes=['bcrypt'], deprecated='auto') # hashing
oauth2_bearer = OAuth2PasswordBearer(tokenUrl='user/login')

access_router = APIRouter()

# database user table
user_db_model.Base.metadata.create_all(bind=engine)

def get_database():
    database = SessionLocal()
    try:
        yield database
    finally:
        database.close()

database_dependency = Annotated[Session, Depends(get_database)]

# Register Endpoints:

@access_router.get('/user/register', tags=['User Register'], response_class=HTMLResponse)
def register_template(request: Request):
    return templates.TemplateResponse('register.html', {
        'request': request
    })

@access_router.post('/user/register', tags=['User Register'], status_code=status.HTTP_201_CREATED, response_class=HTMLResponse)
def create_user(user: Annotated[UserCreate, Form()], 
                 db: database_dependency,
                 request: Request):
    db_user_exists = db.query(Users).filter(Users.userName == user.userName,
                                      Users.userEmail == user.userEmail).first()
    if db_user_exists: raise HTTPException(400, 'User already created')
    if user.userPassword != user.userPasswordConfirm:
        #return RedirectResponse(request.url_for('create_user'), status_code=status.HTTP_400_BAD_REQUEST) 
        raise HTTPException(400, 'Passwords did not match')
    db_user_create = Users(userName = user.userName,
                            userEmail = user.userEmail,
                            userPassword = pswd_context.hash(user.userPasswordConfirm))
    db.add(db_user_create)
    db.commit()
    return RedirectResponse(request.url_for('login_template'), status_code=status.HTTP_303_SEE_OTHER) 

# Login Endpoints:

""" @access_router.get('/user/login', tags=['User Login'], response_class=HTMLResponse)
def login_template(request: Request):
    return templates.TemplateResponse('login.html', {
        'request': request
    }) """

# auth user & hashing pswd
def auth_user(username: str, password: str, db):
    user_data = db.query(Users).filter(Users.userName == username).first()
    if not user_data or not pswd_context.verify(password, user_data.userPassword): return False
    return user_data

# create access token
def create_token(userName: str, userId: int, expires_td: timedelta):
    to_encode = {'sub': userName, 'id': userId}
    expires = datetime.now(timezone.utc) + timedelta(expires_td)
    to_encode.update({'exp': expires})
    return jwt.encode(to_encode, SECRET, algorithm=ALGORITHM)

@access_router.post('/user/login', tags=['User Login'], response_model=Token)
def login_access_token(form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
                       db: database_dependency,):
    user = auth_user(form_data.username, form_data.password, db)
    if not user: raise HTTPException(401, 'Incorrect username or password. Could not validate the user')
    token = create_token(user.userName, user.userId, TOKEN_MINS_EXPIRATION)
    return {'accessToken': token, 'tokenType': 'bearer'}

# Home Endpoints:

@access_router.get('/user/home', tags=['User Home'], response_class=HTMLResponse)
def home_template(request: Request):
    return templates.TemplateResponse('home.html', {
        'request': request
    })

@access_router.get('/user/admin', tags=['Admin'], response_class=HTMLResponse)
def admin_template(request: Request):
    return templates.TemplateResponse('admin.html', {
        'request': request
    })
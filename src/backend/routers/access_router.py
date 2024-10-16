from typing import Annotated
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi import Request, APIRouter, HTTPException, Depends, Form, status
from datetime import timedelta, datetime

from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from passlib.context import CryptContext
from jose import jwt, JWTError

from frontend.templates.templates_router import templates
from backend.database.database_conn import engine, SessionLocal
from backend.base_models.user_base_model import UserBase, UserBaseLogin
from backend.base_models.token_base_model import Token
from backend.database.models import user_db_model
from sqlalchemy.orm import Session

SECRET = 'my-secret-key'
ALGORITHM = 'HS256'
TOKEN_MINS_EXPIRATION = 30

access_router = APIRouter()

user_db_model.Base.metadata.create_all(bind=engine)

def get_database():
    database = SessionLocal()
    try:
        yield database
    finally:
        database.close()

database_dependency = Annotated[Session, Depends(get_database)]

# Register:

pswd_context = CryptContext(schemes=['bcrypt'], deprecated='auto')
oauth2_bearer = OAuth2PasswordBearer(tokenUrl='user/login')

@access_router.get('/user/register', tags=['User Register'], response_class=HTMLResponse)
def register_template(request: Request):
    return templates.TemplateResponse('register.html', {
        'request': request
    })

@access_router.post('/user/register', tags=['User Register'], status_code=status.HTTP_201_CREATED, response_class=HTMLResponse)
def create_user(user: Annotated[UserBase, Form()], 
                 db: database_dependency,
                 request: Request):
    if user.userPassword != user.userPasswordConfirm:
        return RedirectResponse(request.url_for('create_user'), status_code=status.HTTP_400_BAD_REQUEST) 
    db_user = user_db_model.UserDB(userName = user.userName,
                                   userEmail = user.userEmail,
                                   userPassword = pswd_context.hash(user.userPasswordConfirm))
    db.add(db_user)
    db.commit()
    return RedirectResponse(request.url_for('login_template'), status_code=status.HTTP_303_SEE_OTHER) 

# Login:

""" @access_router.post('/token', response_model=Token)
def login_token(form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
                db: database_dependency):
    user_data = auth_user(form_data.userName, form_data.userPassword, db)
    if not user_data: raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)
    token = create_token(user_data.UserDB.userName, user_data.UserDB.userId, timedelta(minutes=30))

def auth_user(userName: str, userPassword: str, db):
    user_data = db.query(user_db_model).filter(user_db_model.UserDB.userName == userName).first()
    if not user_data: return False
    if not pswd_context.verify(userPassword, user_data.userPassword): return False
    return user_data

def create_token(userName: str, userId: int, expires_td: timedelta):
    to_encode = {'sub': userName, 'id': userId}
    expires = datetime.now(datetime.timezone.utc) + expires_td
    to_encode.update({'exp': expires})
    return jwt.encode(to_encode, SECRET, ALGORITHM) """

@access_router.get('/user/login', tags=['User Login'], response_class=HTMLResponse)
def login_template(request: Request):
    return templates.TemplateResponse('login.html', {
        'request': request
    })

@access_router.post('/user/login', tags=['User Login'], response_class=HTMLResponse)
def read_user(user: Annotated[UserBaseLogin, Form()], 
                 db: database_dependency,
                 request: Request,
                 ):
    db_user = db.query(user_db_model.UserDB).filter(user_db_model.UserDB.userName == user.userName,
                                                    user_db_model.UserDB.userPassword == user.userPassword).first()
    if not db_user:
        return RedirectResponse(request.url_for('login_template'), status_code=status.HTTP_303_SEE_OTHER)
    elif db_user.userRole == 'user':
        return RedirectResponse(request.url_for('home_template'), status_code=status.HTTP_303_SEE_OTHER)
    else:
        return RedirectResponse(request.url_for('admin_template'), status_code=status.HTTP_303_SEE_OTHER) 

# Home:

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

""" @access_router.post('/user/register', tags=['User Register'])
async def create_user(user: Annotated[UserBase, Form()], 
                 db: database_dependency,
                 request: Request):
    db_user = user_db_model.UserDB(userName = user.userName,
                                   userEmail = user.userEmail,
                                   userPassword = user.userPassword)
    if user.userPassword != user.userPasswordConfirm: 
        return templates.TemplateResponse('register.html', {
            'request': request,
            'message': HTMLResponse(
                <div class="my-2 d-flex align-items-center justify-content-center container-lg">
                    <div class="alert alert-warning p-2 fs-5" role="alert">
                        Contraseñas no coinciden
                    </div>
                </div>)
        })
    db.add(db_user)
    db.commit() """

### JAJAJAJA 8==> ▄█▀█●
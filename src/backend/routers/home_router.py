from fastapi.responses import HTMLResponse
from fastapi import APIRouter, Request

from frontend.templates.templates_router import templates

home_router = APIRouter()

@home_router.get('/user/home', tags=['Home'], response_class=HTMLResponse)
def home(request: Request):
    return templates.TemplateResponse('home.html', {
        'request': request,
        'message': 'Usuario, bienvenido'
    })
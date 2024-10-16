from fastapi.templating import Jinja2Templates
from os import path

templates_path = path.join(path.dirname(__file__), '../templates')
templates = Jinja2Templates(directory=templates_path)
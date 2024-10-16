from fastapi import FastAPI

from backend.routers.access_router import access_router
from backend.routers.home_router import home_router

app = FastAPI()
app.title, app.version = 'b-management', '1.0'

@app.get('/', tags=['Index'])
def index():
    return 'camellando pa'

app.include_router(access_router)
app.include_router(home_router)
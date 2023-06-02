from fastapi import Depends, FastAPI, Body, HTTPException, Path, Query
from fastapi.responses import HTMLResponse, JSONResponse
from schemas import Movie as MovieSchema, User
from typing import List
from utils.jwt_manager import create_token, validate_token

from fastapi.encoders import jsonable_encoder
from middlewares.jwt_bearer import JWTBearer

from config.database import session, engine, Base
from routers.movie import movie_router
from routers.user import user_router

Base.metadata.create_all(bind=engine)

from middlewares.error_handler import ErrorHandler

app = FastAPI(    
    title="My app with FastAPI",
    description="Aprove using api",
    version="0.1.0",
    terms_of_service="http://example.com/terms/",
    contact={
        "name": "Juan Pablo Mayorga",
        "url": "https://github.com/jpablomayorga",
        "email": "jpablomayorga@gmail.com"
    },
    license_info={
        "name": "Apache 2.0",
        "url": "https://www.apache.org/licenses/LICENSE-2.0.html"}
)
app.add_middleware(ErrorHandler)
app.include_router(movie_router)
app.include_router(user_router)

@app.get('/', tags=['home'])
def message():
    return HTMLResponse('<h2>Hola Juan<h2/>')

@app.post("/login", tags=["auth"], response_model=dict, status_code=200)
def login(user: User):
    if user.email == "admin@gmail.com" and user.password == "admin":
        token: str = create_token(user.dict())
        return JSONResponse(content=token, status_code=200)
    return JSONResponse(content={"message": "usuario o contraseña incorrectos"}, status_code=401)

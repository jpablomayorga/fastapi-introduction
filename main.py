from fastapi import Depends, FastAPI, Body, HTTPException, Path, Query, Request
from fastapi.responses import HTMLResponse, JSONResponse
from schemas import Movie, User
from typing import List
from jwt_manager import create_token, validate_token
from fastapi.security import HTTPBearer

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



movies = [
    {
        'id': 1,
        'title': 'Avatar',
        'overview': "En un exuberante planeta llamado Pandora viven los Na'vi, seres que ...",
        'year': '2009',
        'rating': 7.8,
        'category': 'Acción'    
    },
    {
        'id': 2,
        'title': 'Avatar 2',
        'overview': "En un exuberante planeta llamado Pandora viven los Na'vi, seres que ...",
        'year': '2009',
        'rating': 7.8,
        'category': 'Acción'    
    }       
]

class JWTBearer(HTTPBearer):
    async def __call__(self, request: Request):
        auth = await super().__call__(request)
        data = validate_token(auth.credentials)
        if data['email'] != "admin@gmail.com":
            return HTTPException(status_code=403, detail="Credenciales no son validas")


@app.get('/', tags=['home'])
def message():
    return HTMLResponse('<h2>Hola Juan<h2/>')

@app.post("/login", tags=["auth"], response_model=dict, status_code=200)
def login(user: User):
    if user.email == "admin@gmail.com" and user.password == "admin":
        token: str = create_token(user.dict())
        return JSONResponse(content=token, status_code=200)
    return JSONResponse(content={"message": "usuario o contraseña incorrectos"}, status_code=401)


@app.get("/movies", tags=["movies"], response_model=List[Movie], dependencies=[Depends(JWTBearer())])
def get_movies() -> List[Movie]:
    return JSONResponse(content=movies, status_code=200)

@app.get("/movies/", tags=["movies"], response_model=List[Movie])
def get_movies_by_category(
    category: str = Query(min_length=5, max_length=15,
                          title="Categoria Movie",
                          description="This is the movie category")) -> List[Movie]:
    data = [item for item in movies if item['category'] == category]
    return JSONResponse(content=data, status_code=200)


@app.post("/movies", tags=["movies"], response_model=dict, status_code=201)
def create_movie(movie: Movie) -> dict:
    movies.append(movie)
    return JSONResponse(content={"message": "se ha registrado la pelicula"}, status_code=201)


@app.put("/movies", tags=["movies"], response_model=dict, status_code=200)
def update_movie(
        id: int, movie: Movie) -> dict:
    for item in movies:
        if item['id'] == id:
            item['title'] = movie.title
            item['overview'] = movie.overview
            item['year'] = movie.year
            item['rating'] = movie.rating
            item['category'] = movie.category
    return JSONResponse(content={"message": "se ha actualizado la pelicula"}, status_code=200)


@app.delete("/movies", tags=["movies"], response_model=dict, status_code=200)
def delete_movie(id: int) -> dict:
    for item in movies:
        if item['id'] == id:
            movies.remove(item)
    return JSONResponse(content={"message": "se ha eliminado la pelicula"}, status_code=200)




from fastapi import APIRouter
from schemas import Movie as MovieSchema

from fastapi import Depends, FastAPI, Body, Path, Query, Request
from fastapi.responses import JSONResponse
from schemas import Movie as MovieSchema, User
from typing import List

from fastapi.encoders import jsonable_encoder
from middlewares.jwt_bearer import JWTBearer

from models.models import Movie as MovieModel
from services.movies import MovieService
from config.database import session

movie_router = APIRouter()

@movie_router.get("/movies", tags=["movies"], response_model=List[MovieSchema], dependencies=[Depends(JWTBearer())])
def get_movies() -> List[MovieModel]:
    db = session()
    service = MovieService(db)
    movies = service.get_movies()
    print('total: ', len(movies))
    return JSONResponse(content=jsonable_encoder(movies), status_code=200)

@movie_router.get('/movies/{id}', tags=['movies'], response_model= MovieSchema)
def get_movie(id: int = Path(ge=1, le=2000)) -> MovieModel:
    db = session()
    service = MovieService(db)
    movie = service.get_movie(id)
    if not movie:
        return JSONResponse(content={'message': 'no encontrado'}, status_code=404)
    return JSONResponse(content=jsonable_encoder(movie), status_code=200)

@movie_router.get("/movies/", tags=["movies"], response_model=List[MovieSchema])
def get_movies_by_category(
    category: str = Query(min_length=5, max_length=15,
                          title="Categoria Movie",
                          description="This is the movie category")) -> List[MovieModel]:
    db = session()
    service = MovieService(db)
    movies = service.get_movie_by_category(category)
    return JSONResponse(content=jsonable_encoder(movies), status_code=200)
    

@movie_router.post("/movies", tags=["movies"], response_model=dict, status_code=201)
def create_movie(movie: MovieSchema) -> dict:
    db = session()
    # new_movie = MovieModel(**movie.dict())
    # db.add(new_movie)
    # db.commit()
    service = MovieService(db)
    movies = service.create_movie(movie)

    return JSONResponse(content={"message": "se ha registrado la pelicula"}, status_code=201)


@movie_router.put("/movies/{id}", tags=["movies"], response_model=dict, status_code=200)
def update_movie(id: int, movie: MovieSchema) -> dict:
    db = session()
    service = MovieService(db)
    result = service.get_movie(id)
    if not result:
        return JSONResponse(content={'message': 'no encontrado'}, status_code=404)    
    movies = service.update_movie(id, movie) 
    return JSONResponse(content={"message": "se ha actualizado la pelicula"}, status_code=200)


@movie_router.delete("/movies/{id}", tags=["movies"], response_model=dict, status_code=200)
def delete_movie(id: int) -> dict:
    db = session()
    service = MovieService(db)
    result = service.get_movie(id)
    if not result:
        return JSONResponse(content={'message': 'no encontrado'}, status_code=404)
    service.delete_movie(id)
    return JSONResponse(content={"message": "se ha eliminado la pelicula"}, status_code=200)
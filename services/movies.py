from models.models import Movie as MovieModel
from schemas import Movie as MovieSchema


class MovieService():
    def __init__(self, db) -> None:
        self.db = db
    
    def get_movies(self):
        result = self.db.query(MovieModel).all()
        return result
    
    def get_movie(self, id):
        return self.db.query(MovieModel).filter(MovieModel.id == id).first()
    
    def get_movie_by_category(self, category):
        return self.db.query(MovieModel).filter(MovieModel.category == category).all()
    
    def create_movie(self, movie: MovieSchema):
        new_movie = MovieModel(**movie.dict())
        self.db.add(new_movie)
        self.db.commit()
        return

    def update_movie(self, id: int, data: MovieSchema):
        result = self.db.query(MovieModel).filter(MovieModel.id == id).first()        
        result.title = data.title
        result.overview = data.overview
        result.category = data.category
        result.rating = data.rating
        result.year = data.year
        self.db.commit()
        return
    
    def delete_movie(self, id:int):
        self.db.query(MovieModel).filter(MovieModel.id == id).delete()
        self.db.commit()
        return





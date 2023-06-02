from sqlalchemy import Column, Float, Integer, String
from sqlalchemy.orm import relationship

from config.database import Base


class Movie(Base):
    __tablename__ = "movies"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, unique=True, index=True)
    overview = Column(String)
    year = Column(Integer)
    rating = Column(Float)
    category = Column(String)   

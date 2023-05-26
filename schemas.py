from pydantic import BaseModel, Field
from typing import Optional

from pydantic import BaseModel, Field

class Movie(BaseModel):
    id: Optional[int] = None
    title: str = Field(min_length=5, max_length=15)
    overview: str = Field(min_length=15, max_length=50)
    year: int = Field(ge=1900, le=2021)
    rating: float = Field(ge=0.0, le=10.0)
    category: str = Field(min_length=5, max_length=15)

    class Config:
        schema_extra = {
            "example": {
                "title": "Mi pelicula",
                "overview": "Descripcion de mi pelicula ...",
                "year": 2000,
                "rating": 5.0,
                "category": "Acción"
            }
        }

class User(BaseModel):
    email: str = Field(min_length=5, max_length=100,title="Email",
                    description="This is the email")
    password: str = Field(min_length=5, max_length=15,
                        title="Password",
                        description="This is the password")
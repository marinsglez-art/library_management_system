from datetime import datetime, date, time
from typing import Any, List, Optional, Union, Set
from enum import Enum
from pydantic import BaseModel, field_validator


############################################
# Enumerations are defined here
############################################

class Genre(Enum):
    Adventure = "Adventure"
    Technology = "Technology"
    Poetry = "Poetry"
    Fantasy = "Fantasy"
    Philosophy = "Philosophy"
    Cookbooks = "Cookbooks"
    Thriller = "Thriller"
    History = "History"
    Horror = "Horror"
    Romance = "Romance"

############################################
# Classes are defined here
############################################
class AuthorCreate(BaseModel):
    birth: date
    name: str
    books: Optional[List[int]] = None  # N:M Relationship (optional)


class LibraryCreate(BaseModel):
    telephone: str
    web_page: str
    address: str
    name: str
    books: Optional[List[int]] = None  # N:M Relationship (optional)


class BookCreate(BaseModel):
    release: date
    title: str
    pages: int
    genre: Genre
    stock: int
    price: float
    library: List[int]  # N:M Relationship
    authors: List[int]  # N:M Relationship

    @field_validator('pages')
    @classmethod
    def validate_pages_1(cls, v):
        """OCL Constraint: constraint_Book_0_1"""
        if not (v > 10):
            raise ValueError('pages must be > 10')
        return v


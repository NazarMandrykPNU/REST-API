from pydantic import BaseModel, Field
from typing import Optional

class BookBase(BaseModel):
    """Base model for book data."""
    title: str = Field(..., min_length=1, max_length=200)
    author: str = Field(..., min_length=1, max_length=200)
    year: int = Field(..., ge=1000, le=2024)

class BookCreate(BookBase):
    """Model for creating a new book."""
    pass

class Book(BookBase):
    """Model for book response."""
    id: int

    class Config:
        from_attributes = True 
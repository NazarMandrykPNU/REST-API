from fastapi import FastAPI, HTTPException
from typing import List
from .models import Book, BookCreate

app = FastAPI(
    title="Library API",
    description="A simple FastAPI-based REST API for managing a library's book collection",
    version="1.0.0"
)


books = [
    {
        "id": 1,
        "title": "The Great Gatsby",
        "author": "F. Scott Fitzgerald",
        "year": 1925
    },
    {
        "id": 2,
        "title": "To Kill a Mockingbird",
        "author": "Harper Lee",
        "year": 1960
    },
    {
        "id": 3,
        "title": "1984",
        "author": "George Orwell",
        "year": 1949
    },
    {
        "id": 4,
        "title": "Pride and Prejudice",
        "author": "Jane Austen",
        "year": 1813
    },
    {
        "id": 5,
        "title": "The Hobbit",
        "author": "J.R.R. Tolkien",
        "year": 1937
    }
]

next_id = len(books) + 1


@app.get("/api/books", response_model=List[Book])
async def get_books():
    """Get all books"""
    return books


@app.get("/api/books/{book_id}", response_model=Book)
async def get_book(book_id: int):
    """Retrieve"""
    book = next((book for book in books if book["id"] == book_id), None)
    if book is None:
        raise HTTPException(status_code=404, detail="Book not found")
    return book


@app.post("/api/books", response_model=Book, status_code=201)
async def create_book(book: BookCreate):
    """Add a new book"""
    global next_id
    new_book = {
        "id": next_id,
        "title": book.title,
        "author": book.author,
        "year": book.year
    }
    books.append(new_book)
    next_id += 1
    return new_book


@app.delete("/api/books/{book_id}", status_code=204)
async def delete_book(book_id: int):
    """Delete a book by ID."""
    global books
    initial_length = len(books)
    books = [book for book in books if book["id"] != book_id]
    
    if len(books) == initial_length:
        raise HTTPException(status_code=404, detail="Book not found")
    
    return None 
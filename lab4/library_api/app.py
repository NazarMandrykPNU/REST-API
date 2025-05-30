import os
from flask import Blueprint, request, jsonify
from marshmallow import ValidationError
from sqlalchemy import desc

from .models import db, Book
from .schemas import BookSchema, BookPaginationSchema

main = Blueprint('main', __name__)

# Schema instances
book_schema = BookSchema()
books_schema = BookSchema(many=True)
pagination_schema = BookPaginationSchema()

@main.route('/api/books', methods=['GET'])
def get_books():
    """Get all books with cursor-based pagination
    ---
    get:
      summary: Get all books
      description: Returns a list of books with cursor-based pagination
      parameters:
        - in: query
          name: cursor
          schema:
            type: integer
          description: ID of the last book from previous page
        - in: query
          name: per_page
          schema:
            type: integer
            default: 10
          description: Number of books per page
      responses:
        200:
          description: A list of books
          content:
            application/json:
              schema: BookPaginationSchema
        400:
          description: Invalid parameters
    """
    cursor = request.args.get('cursor', type=int)
    per_page = request.args.get('per_page', 10, type=int)
    
    # Validate pagination parameters
    if per_page < 1 or per_page > 100:
        return jsonify({'error': 'Items per page must be between 1 and 100'}), 400
    
    # Base query
    query = Book.query.order_by(desc(Book.id))
    
    # Apply cursor if provided
    if cursor:
        query = query.filter(Book.id < cursor)
    
    # Get books for current page
    books = query.limit(per_page + 1).all()
    
    # Check if there are more items
    has_more = len(books) > per_page
    if has_more:
        books = books[:-1]  # Remove the extra item
    
    # Get next cursor
    next_cursor = books[-1].id if books else None
    
    # Prepare response
    response = {
        'items': books_schema.dump(books),
        'next_cursor': next_cursor,
        'has_more': has_more
    }
    
    return jsonify(response)

@main.route('/api/books/<int:book_id>', methods=['GET'])
def get_book(book_id):
    """Get a specific book by ID
    ---
    get:
      summary: Get a book by ID
      description: Returns a single book by its ID
      parameters:
        - in: path
          name: book_id
          required: true
          schema:
            type: integer
          description: ID of the book to get
      responses:
        200:
          description: A book
          content:
            application/json:
              schema: BookSchema
        404:
          description: Book not found
    """
    book = Book.query.get_or_404(book_id)
    return jsonify(book_schema.dump(book))

@main.route('/api/books', methods=['POST'])
def create_book():
    """Create a new book
    ---
    post:
      summary: Create a new book
      description: Creates a new book
      requestBody:
        required: true
        content:
          application/json:
            schema: BookSchema
      responses:
        201:
          description: Book created
          content:
            application/json:
              schema: BookSchema
        400:
          description: Invalid input
    """
    try:
        data = book_schema.load(request.json)
        book = Book(**data)
        db.session.add(book)
        db.session.commit()
        return jsonify(book_schema.dump(book)), 201
    except ValidationError as err:
        return jsonify({'error': err.messages}), 400

@main.route('/api/books/<int:book_id>', methods=['DELETE'])
def delete_book(book_id):
    """Delete a book
    ---
    delete:
      summary: Delete a book
      description: Deletes a book by its ID
      parameters:
        - in: path
          name: book_id
          required: true
          schema:
            type: integer
          description: ID of the book to delete
      responses:
        204:
          description: Book deleted
        404:
          description: Book not found
    """
    book = Book.query.get_or_404(book_id)
    db.session.delete(book)
    db.session.commit()
    return '', 204 

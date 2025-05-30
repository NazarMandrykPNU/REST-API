from flask import Flask, request, jsonify
from marshmallow import ValidationError

from .schema import BookSchema

app = Flask(__name__)


books = [
    {
        'id': 1,
        'title': 'The Great Gatsby',
        'author': 'F. Scott Fitzgerald',
        'year': 1925
    },
    {
        'id': 2,
        'title': 'To Kill a Mockingbird',
        'author': 'Harper Lee',
        'year': 1960
    },
    {
        'id': 3,
        'title': '1984',
        'author': 'George Orwell',
        'year': 1949
    },
    {
        'id': 4,
        'title': 'Pride and Prejudice',
        'author': 'Jane Austen',
        'year': 1813
    },
    {
        'id': 5,
        'title': 'The Hobbit',
        'author': 'J.R.R. Tolkien',
        'year': 1937
    }
]

next_id = len(books) + 1

# Schema instances
book_schema = BookSchema()
books_schema = BookSchema(many=True)


@app.route('/api/books', methods=['GET'])
def get_books():
    """Get all books"""
    return jsonify(books_schema.dump(books))


@app.route('/api/books/<int:book_id>', methods=['GET'])
def get_book(book_id):
    """Retrieve"""
    book = next((book for book in books if book['id'] == book_id), None)
    if book is None:
        return jsonify({'error': 'Book not found'}), 404
    return jsonify(book_schema.dump(book))


@app.route('/api/books', methods=['POST'])
def add_book():
    """Add a new book"""
    global next_id
    
    try:
        # Validate
        data = book_schema.load(request.json)
        
        # Create new book
        new_book = {
            'id': next_id,
            'title': data['title'],
            'author': data['author'],
            'year': data['year']
        }
        
        books.append(new_book)
        next_id += 1
        
        return jsonify(book_schema.dump(new_book)), 201
        
    except ValidationError as err:
        return jsonify({'error': err.messages}), 400


@app.route('/api/books/<int:book_id>', methods=['DELETE'])
def delete_book(book_id):
    """Delete a book by ID"""
    global books
    initial_length = len(books)
    books = [book for book in books if book['id'] != book_id]
    
    if len(books) == initial_length:
        return jsonify({'error': 'Book not found'}), 404
        
    return '', 204


def create_app():
    """Create and configure the Flask application"""
    return app 
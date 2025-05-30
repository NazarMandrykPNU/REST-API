from .app import create_app
from .models import db, Book

def init_db():
    app = create_app()
    with app.app_context():
        # Clear existing data
        Book.query.delete()
        
        # Sample books
        books = [
            Book(
                title="The Great Gatsby",
                author="F. Scott Fitzgerald",
                year=1925
            ),
            Book(
                title="To Kill a Mockingbird",
                author="Harper Lee",
                year=1960
            ),
            Book(
                title="1984",
                author="George Orwell",
                year=1949
            ),
            Book(
                title="Pride and Prejudice",
                author="Jane Austen",
                year=1813
            ),
            Book(
                title="The Hobbit",
                author="J.R.R. Tolkien",
                year=1937
            ),
            Book(
                title="The Lord of the Rings",
                author="J.R.R. Tolkien",
                year=1954
            ),
            Book(
                title="The Catcher in the Rye",
                author="J.D. Salinger",
                year=1951
            ),
            Book(
                title="The Little Prince",
                author="Antoine de Saint-Exupéry",
                year=1943
            ),
            Book(
                title="The Alchemist",
                author="Paulo Coelho",
                year=1988
            ),
            Book(
                title="The Da Vinci Code",
                author="Dan Brown",
                year=2003
            )
        ]
        
        # Add books to database
        for book in books:
            db.session.add(book)
        
        # Commit changes
        db.session.commit()
        print("Database initialized with sample books!")

if __name__ == "__main__":
    init_db() 
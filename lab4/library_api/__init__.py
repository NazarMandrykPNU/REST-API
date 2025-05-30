"""
Library API package for managing books using Flask and PostgreSQL.
"""
import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

db = SQLAlchemy()
migrate = Migrate()

def create_app():
    app = Flask(__name__)
    
    # Налаштування бази даних
    app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('SQLALCHEMY_DATABASE_URI', 'postgresql://postgres:postgres@db:5432/library')
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    
    # Ініціалізація розширень
    db.init_app(app)
    migrate.init_app(app, db)
    
    # Імпортуємо моделі тут, після ініціалізації db
    from . import models
    
    # Реєстрація blueprints
    from .app import main
    app.register_blueprint(main)
    
    # Створення таблиць при старті
    with app.app_context():
        db.create_all()
    
    return app 
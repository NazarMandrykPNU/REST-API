"""
Library API package for managing books using Flask and PostgreSQL.
"""
import os
from flask import Flask, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from apispec import APISpec
from apispec.ext.marshmallow import MarshmallowPlugin
from apispec_webframeworks.flask import FlaskPlugin
from flask_swagger_ui import get_swaggerui_blueprint

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

    # Налаштування Swagger
    spec = APISpec(
        title="Library API",
        version="1.0.0",
        openapi_version="3.0.2",
        plugins=[FlaskPlugin(), MarshmallowPlugin()],
    )

    # Додаємо схеми в Swagger
    from .schemas import BookSchema, BookPaginationSchema
    spec.components.schema("Book", schema=BookSchema)
    spec.components.schema("BookPagination", schema=BookPaginationSchema)

    # Додаємо шляхи в Swagger (після реєстрації blueprint)
    with app.test_request_context():
        spec.path(view=app.view_functions['main.get_books'])
        spec.path(view=app.view_functions['main.get_book'])
        spec.path(view=app.view_functions['main.create_book'])
        spec.path(view=app.view_functions['main.delete_book'])

    # Створюємо Swagger UI blueprint
    swaggerui_blueprint = get_swaggerui_blueprint(
        '/swagger',
        '/swagger.json',
        config={
            'app_name': "Library API Documentation"
        }
    )
    app.register_blueprint(swaggerui_blueprint, url_prefix='/swagger')

    # Додаємо endpoint для swagger.json
    @app.route("/swagger.json")
    def create_swagger_spec():
        return jsonify(spec.to_dict())
    
    # Створення таблиць при старті
    with app.app_context():
        db.create_all()
    
    return app 

# app/__init__.py
from flask import Flask
from flask_assets import Environment
from werkzeug.middleware.proxy_fix import ProxyFix
import os

from app.config import config_by_name

def create_app(config_name='development'):
    """Factory pattern to create the Flask application."""
    app = Flask(__name__)
    
    # Load configuration based on environment name
    app.config.from_object(config_by_name[config_name])
    
    # Support for proxies in production (helps with proper URL generation)
    app.wsgi_app = ProxyFix(app.wsgi_app, x_for=1, x_proto=1)
    
    # Initialize Flask extensions
    assets = Environment(app)
    
    # Register blueprints
    from app.routes.main import main_bp
    app.register_blueprint(main_bp)
    
    # Initialize services
    from app.services.notebook_service import init_notebook_service
    init_notebook_service(app)

    # Register context processors
    from app.context_processors import register_context_processors
    register_context_processors(app)
    
    # Configure logging
    if not app.debug:
        import logging
        from logging.handlers import RotatingFileHandler
        
        if not os.path.exists('logs'):
            os.mkdir('logs')
            
        file_handler = RotatingFileHandler(
            'logs/python_notes.log', 
            maxBytes=10240, 
            backupCount=10
        )
        file_handler.setFormatter(logging.Formatter(
            '%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]'
        ))
        file_handler.setLevel(logging.INFO)
        
        app.logger.addHandler(file_handler)
        app.logger.setLevel(logging.INFO)
        app.logger.info('Python Notes Website startup')
    
    return app
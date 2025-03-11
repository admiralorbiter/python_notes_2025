# app/context_processors.py
from datetime import datetime

def inject_now():
    """Add the current datetime to the template context."""
    return {'now': datetime.utcnow()}

def register_context_processors(app):
    """Register all context processors with the Flask app."""
    app.context_processor(inject_now)
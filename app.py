#!/usr/bin/env python
"""
Main application entry point for Python Notes Website.
Run this file directly to start the development server:
    python app.py
"""

import os
from app import create_app

# Determine environment from environment variable or default to development
config_name = os.environ.get('FLASK_ENV', 'development')
app = create_app(config_name)

if __name__ == '__main__':
    # Load notebooks from the notebooks directory
    print(f"Loading notebooks from: {app.config['NOTEBOOKS_DIR']}")
    
    # Development server configuration
    host = os.environ.get('HOST', '127.0.0.1')
    port = int(os.environ.get('PORT', 5000))
    debug = app.config.get('DEBUG', True)
    
    print(f"Starting development server at http://{host}:{port}")
    print(f"Debug mode: {'on' if debug else 'off'}")
    print("Press CTRL+C to quit")
    
    app.run(host=host, port=port, debug=debug)
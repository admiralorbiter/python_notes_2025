# wsgi.py
import os
from app import create_app

# Determine environment from environment variable or default to production
config_name = os.environ.get('FLASK_ENV', 'production')
app = create_app(config_name)

if __name__ == '__main__':
    app.run(host='0.0.0.0')
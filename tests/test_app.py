# tests/test_app.py
import os
import pytest
from app import create_app

@pytest.fixture
def app():
    """Create and configure a Flask app for testing."""
    # Create the app with the testing configuration
    app = create_app('testing')
    
    # Create a test notebook directory if it doesn't exist
    notebooks_dir = app.config['NOTEBOOKS_DIR']
    if not os.path.exists(notebooks_dir):
        os.makedirs(notebooks_dir)
    
    # Create a dummy notebook for testing if needed
    # This would be implemented for more comprehensive tests
    
    yield app
    
    # Clean up code if needed

@pytest.fixture
def client(app):
    """A test client for the app."""
    return app.test_client()

def test_home_page(client):
    """Test that the home page loads successfully."""
    response = client.get('/')
    assert response.status_code == 200
    assert b"Python Interactive Notes" in response.data

def test_about_page(client):
    """Test that the about page loads successfully."""
    response = client.get('/about')
    assert response.status_code == 200
    assert b"About Python Notes" in response.data

def test_404_page(client):
    """Test that the 404 page works."""
    response = client.get('/nonexistent-page')
    assert response.status_code == 404
    assert b"404 - Page Not Found" in response.data

# More comprehensive tests would be added for:
# - Notebook rendering
# - Code execution
# - Static file serving
# - etc.
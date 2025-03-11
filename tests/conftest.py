# tests/conftest.py
import os
import tempfile
import pytest
import shutil
import json

# Import the app factory
from app import create_app

@pytest.fixture(scope='session')
def test_notebook_dir():
    """Create a temporary directory for test notebooks."""
    test_dir = tempfile.mkdtemp()
    
    # Create a simple test notebook file
    notebook_content = {
        "metadata": {
            "kernelspec": {
                "display_name": "Python 3",
                "language": "python",
                "name": "python3"
            },
            "language_info": {
                "codemirror_mode": {
                    "name": "ipython",
                    "version": 3
                },
                "file_extension": ".py",
                "mimetype": "text/x-python",
                "name": "python",
                "nbconvert_exporter": "python",
                "pygments_lexer": "ipython3",
                "version": "3.8.0"
            }
        },
        "nbformat": 4,
        "nbformat_minor": 4,
        "cells": [
            {
                "cell_type": "markdown",
                "metadata": {},
                "source": [
                    "# Test Notebook\n",
                    "\n",
                    "This is a test notebook for unit tests."
                ]
            },
            {
                "cell_type": "code",
                "execution_count": null,
                "metadata": {},
                "outputs": [],
                "source": [
                    "# This is a test code cell\n",
                    "print('Hello, world!')"
                ]
            },
            {
                "cell_type": "code",
                "execution_count": null,
                "metadata": {},
                "outputs": [],
                "source": [
                    "# Another test cell\n",
                    "a = 5\n",
                    "b = 10\n",
                    "print(f'The sum is {a + b}')"
                ]
            }
        ]
    }
    
    # Write the test notebook to the temporary directory
    with open(os.path.join(test_dir, 'test_notebook.ipynb'), 'w') as f:
        json.dump(notebook_content, f)
    
    yield test_dir
    
    # Cleanup after tests
    shutil.rmtree(test_dir)

@pytest.fixture
def app(test_notebook_dir):
    """Create and configure a Flask app for testing."""
    # Use the testing configuration
    app = create_app('testing')
    
    # Override the NOTEBOOKS_DIR to use our temporary test directory
    app.config['NOTEBOOKS_DIR'] = test_notebook_dir
    
    # Create a test context
    with app.app_context():
        yield app

@pytest.fixture
def client(app):
    """A test client for the app."""
    return app.test_client()

@pytest.fixture
def runner(app):
    """A test CLI runner for the app."""
    return app.test_cli_runner()
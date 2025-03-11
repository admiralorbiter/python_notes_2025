# Python Notes Website

An interactive website for hosting Python educational content from Jupyter notebooks. Students can read course materials and execute Python code directly in their browser.

## Features

- Convert Jupyter notebooks into interactive web pages
- Run Python code directly in the browser using PyScript
- Clean, responsive design for all devices
- Easy navigation between lessons
- Copy code snippets with a single click
- Table of contents for longer lessons

## Getting Started

### Prerequisites

- Python 3.8 or higher
- pip (Python package installer)

### Installation

1. Clone the repository
   ```bash
   git clone <repository-url>
   cd python_notes_website
   ```

2. Create and activate a virtual environment
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows, use `venv\Scripts\activate`
   ```

3. Install dependencies
   ```bash
   pip install -r requirements.txt
   ```

4. Create a `.env` file with configuration (example)
   ```
   FLASK_APP=wsgi.py
   FLASK_ENV=development
   SECRET_KEY=your-secret-key-here
   ```

### Running Locally

```bash
flask run
```

The application will be available at http://127.0.0.1:5000

### Adding Notebooks

1. Place your Jupyter notebook files (`.ipynb`) in the `notebooks` directory
2. The application will automatically discover and display them

## Deployment to PythonAnywhere

1. Sign in to your PythonAnywhere account

2. Open a Bash console and clone your repository
   ```bash
   git clone <repository-url>
   cd python_notes_website
   ```

3. Create a virtual environment and install dependencies
   ```bash
   python -m venv venv
   source venv/bin/activate
   pip install -r requirements.txt
   ```

4. Configure a new web app in the PythonAnywhere dashboard:
   - Choose "Manual configuration" and select your Python version
   - Set the path to your virtual environment
   - Configure the WSGI file to point to `wsgi.py`

5. Set up environment variables in the PythonAnywhere dashboard under the "Web" tab

6. Reload your web app

## Project Structure

```
python_notes_website/
│
├── app/                          # Application package
│   ├── __init__.py               # Flask application factory
│   ├── config.py                 # Configuration settings
│   ├── routes/                   # Route definitions
│   ├── services/                 # Business logic
│   ├── static/                   # Static files
│   └── templates/                # Jinja2 templates
│
├── notebooks/                    # Source notebooks
│
├── tests/                        # Test directory
│
├── .env                          # Environment variables
├── requirements.txt              # Project dependencies
└── wsgi.py                       # WSGI entry point for production
```
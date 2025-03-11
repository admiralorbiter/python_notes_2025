# app/routes/main.py
from flask import Blueprint, render_template, current_app, abort, send_from_directory, request, redirect, url_for
import os
import glob
from app.services.notebook_service import get_notebook_html, get_notebook_metadata

main_bp = Blueprint('main', __name__)

@main_bp.route('/')
def index():
    """Home page route that displays available notebooks."""
    notebooks_dir = current_app.config['NOTEBOOKS_DIR']
    notebook_files = glob.glob(os.path.join(notebooks_dir, '*.ipynb'))
    
    notebooks = []
    for notebook_path in notebook_files:
        filename = os.path.basename(notebook_path)
        notebook_id = os.path.splitext(filename)[0]
        
        # Get metadata for display
        metadata = get_notebook_metadata(notebook_path)
        title = metadata.get('title', notebook_id)
        
        notebooks.append({
            'id': notebook_id,
            'title': title,
            'path': notebook_path,
            'filename': filename
        })
    
    # Sort notebooks by title
    notebooks.sort(key=lambda x: x['title'])
    
    return render_template('index.html', notebooks=notebooks)

@main_bp.route('/notes/<notebook_id>')
def view_notebook(notebook_id):
    """Display a specific notebook."""
    notebooks_dir = current_app.config['NOTEBOOKS_DIR']
    notebook_path = os.path.join(notebooks_dir, f"{notebook_id}.ipynb")
    
    if not os.path.isfile(notebook_path):
        abort(404)
    
    # Convert notebook to HTML
    html_content, resources = get_notebook_html(notebook_path)
    
    # Get metadata
    metadata = get_notebook_metadata(notebook_path)
    title = metadata.get('title', notebook_id)
    
    return render_template(
        'notes/view.html',
        notebook_id=notebook_id,
        title=title,
        html_content=html_content,
        pyscript_enabled=current_app.config.get('PYSCRIPT_ENABLED', True)
    )

@main_bp.route('/static/notebooks/<path:filename>')
def notebook_static(filename):
    """Serve static files associated with notebooks."""
    notebooks_dir = current_app.config.get('NOTEBOOKS_DIR')
    return send_from_directory(notebooks_dir, filename)

@main_bp.route('/about')
def about():
    """About page."""
    return render_template('about.html', title="About")

@main_bp.app_errorhandler(404)
def page_not_found(e):
    """Custom 404 page."""
    return render_template('error/404.html'), 404

@main_bp.app_errorhandler(500)
def server_error(e):
    """Custom 500 page."""
    return render_template('error/500.html'), 500
# app/services/notebook_service.py
import os
import json
import nbformat
from nbconvert import HTMLExporter
from nbconvert.preprocessors import ExecutePreprocessor
from flask import current_app
from traitlets.config import Config

# Global exporter object
html_exporter = None
execute_preprocessor = None

def init_notebook_service(app):
    """Initialize the notebook service with app context."""
    global html_exporter, execute_preprocessor
    
    # Configure the HTML exporter
    c = Config()
    c.HTMLExporter.exclude_input_prompt = True
    c.HTMLExporter.exclude_output_prompt = True
    c.HTMLExporter.template_name = 'classic'
    
    html_exporter = HTMLExporter(config=c)
    
    # Configure the execute preprocessor for potential future use
    execute_preprocessor = ExecutePreprocessor(timeout=600, kernel_name='python3')
    
    app.logger.info('Notebook service initialized')

def get_notebook_metadata(notebook_path):
    """Extract metadata from a notebook file."""
    try:
        with open(notebook_path, 'r', encoding='utf-8') as f:
            notebook_content = json.load(f)
            
        # Extract basic metadata
        metadata = {}
        
        # Get notebook title from the first markdown cell if it exists
        if 'cells' in notebook_content and len(notebook_content['cells']) > 0:
            first_cell = notebook_content['cells'][0]
            if first_cell['cell_type'] == 'markdown' and first_cell['source']:
                # Look for a title in the first line
                first_line = first_cell['source'][0] if isinstance(first_cell['source'], list) else first_cell['source'].split('\n')[0]
                if first_line.startswith('# '):
                    metadata['title'] = first_line[2:].strip()
        
        # Use filename as fallback for title
        if 'title' not in metadata:
            metadata['title'] = os.path.splitext(os.path.basename(notebook_path))[0]
            
        return metadata
        
    except Exception as e:
        current_app.logger.error(f"Error extracting metadata from {notebook_path}: {str(e)}")
        return {'title': os.path.splitext(os.path.basename(notebook_path))[0]}

def get_notebook_html(notebook_path):
    """Convert notebook to JupyterLite compatible HTML."""
    with open(notebook_path, 'r', encoding='utf-8') as f:
        notebook = nbformat.read(f, as_version=4)
    
    # Configure the HTML exporter for JupyterLite compatibility
    c = Config()
    c.HTMLExporter.template_name = 'classic'
    c.HTMLExporter.exclude_input_prompt = True
    c.HTMLExporter.exclude_output_prompt = True
    c.HTMLExporter.embed_images = True
    
    html_exporter = HTMLExporter(config=c)
    html_content, resources = html_exporter.from_notebook_node(notebook)
    
    return html_content, resources

def add_interactive_elements(html_content):
    """Enhance HTML with PyScript for interactive execution."""
    # Add data-executable attribute to code cells
    html_content = html_content.replace('<div class="input_area">', 
                                         '<div class="input_area" data-executable="true">')
    
    # Add run button to each code cell
    html_content = html_content.replace('<div class="input_area" data-executable="true">',
                                         '<div class="input_area" data-executable="true">'
                                         '<button class="run-code-btn">Run</button>')
    
    return html_content
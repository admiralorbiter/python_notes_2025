# app/services/notebook_service.py
import os
import json
import nbformat
from nbconvert import HTMLExporter
from nbconvert.preprocessors import ExecutePreprocessor, Preprocessor
from flask import current_app
from traitlets.config import Config
import shutil

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
    """Get metadata from notebook file."""
    with open(notebook_path, 'r', encoding='utf-8') as f:
        notebook = nbformat.read(f, as_version=4)
        
        # Get title from first cell if it's markdown
        title = None
        if notebook.cells and notebook.cells[0].cell_type == 'markdown':
            first_line = notebook.cells[0].source.split('\n')[0]
            # Remove markdown heading symbols and whitespace
            title = first_line.lstrip('#').strip()
        
        if not title:
            # Fallback to filename
            title = os.path.splitext(os.path.basename(notebook_path))[0]
            
        return {
            'title': title,
            'metadata': notebook.metadata
        }

class CodeCellPreprocessor(Preprocessor):
    """Custom preprocessor to mark code cells as executable."""
    
    def preprocess_cell(self, cell, resources, cell_index):
        """Preprocess cell to add executable markers."""
        if cell['cell_type'] == 'code':
            cell['source'] = f'<div class="code-cell">{cell["source"]}</div>'
        return cell, resources

def get_notebook_html(notebook_path):
    """Convert notebook to HTML with interactive features."""
    with open(notebook_path, 'r', encoding='utf-8') as f:
        notebook = nbformat.read(f, as_version=4)
    
    # Configure the HTML exporter
    html_exporter = HTMLExporter()
    html_exporter.template_name = 'classic'
    
    # Remove the first cell if it's the same as the title
    if notebook.cells and notebook.cells[0].cell_type == 'markdown':
        first_cell_text = notebook.cells[0].source.strip()
        if first_cell_text.startswith('# '):
            notebook.cells.pop(0)
    
    # Convert notebook to HTML
    html_content, resources = html_exporter.from_notebook_node(notebook)
    
    # Save resources (images, etc.) if needed
    if resources.get('outputs'):
        static_dir = os.path.join(current_app.static_folder, 'notebooks')
        os.makedirs(static_dir, exist_ok=True)
        
        for filename, data in resources['outputs'].items():
            with open(os.path.join(static_dir, filename), 'wb') as f:
                f.write(data)
    
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
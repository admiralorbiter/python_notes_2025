#!/usr/bin/env python
"""
Notebook Conversion Tool
This script helps convert Jupyter notebooks to HTML for testing outside the web app.
"""

import os
import sys
import argparse
import nbformat
from nbconvert import HTMLExporter
from traitlets.config import Config

def convert_notebook(notebook_path, output_dir=None, execute=False):
    """Convert a notebook to HTML."""
    try:
        # Check if file exists
        if not os.path.exists(notebook_path):
            print(f"Error: File not found: {notebook_path}")
            return False
        
        # Read the notebook
        with open(notebook_path, 'r', encoding='utf-8') as f:
            notebook = nbformat.read(f, as_version=4)
        
        # Configure the HTML exporter
        c = Config()
        c.HTMLExporter.exclude_input_prompt = True
        c.HTMLExporter.exclude_output_prompt = True
        c.HTMLExporter.template_name = 'classic'
        
        html_exporter = HTMLExporter(config=c)
        
        # Convert to HTML
        (html_content, resources) = html_exporter.from_notebook_node(notebook)
        
        # Determine output filename
        base_name = os.path.basename(notebook_path)
        name_without_ext = os.path.splitext(base_name)[0]
        
        # Determine output directory
        if output_dir is None:
            output_dir = os.path.dirname(notebook_path)
        
        if not os.path.exists(output_dir):
            os.makedirs(output_dir)
        
        output_path = os.path.join(output_dir, f"{name_without_ext}.html")
        
        # Write HTML to file
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(html_content)
        
        print(f"Successfully converted {notebook_path} to {output_path}")
        return True
        
    except Exception as e:
        print(f"Error converting notebook: {str(e)}")
        return False

def main():
    """Parse command line arguments and convert notebooks."""
    parser = argparse.ArgumentParser(description='Convert Jupyter notebooks to HTML.')
    parser.add_argument('notebook', help='Path to the notebook file (.ipynb)')
    parser.add_argument('-o', '--output-dir', help='Output directory (default: same as notebook)')
    parser.add_argument('-e', '--execute', action='store_true', help='Execute notebook before converting')
    
    args = parser.parse_args()
    
    success = convert_notebook(args.notebook, args.output_dir, args.execute)
    
    if not success:
        sys.exit(1)

if __name__ == '__main__':
    main()
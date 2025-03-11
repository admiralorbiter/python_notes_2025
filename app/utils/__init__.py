def is_valid_notebook(filename):
    """Check if a file is a valid Jupyter notebook."""
    return filename.endswith('.ipynb')

def get_notebook_id(filename):
    """Extract notebook ID from filename."""
    return filename.rsplit('.', 1)[0]
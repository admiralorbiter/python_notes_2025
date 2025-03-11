#!/usr/bin/env python
"""Setup script for Python Notes Website."""

import os
import shutil
import subprocess
from pathlib import Path

def setup_environment():
    """Setup the application environment."""
    print("Setting up Python Notes Website...")
    
    # Create .env file if it doesn't exist
    if not os.path.exists('.env'):
        shutil.copy('.env.example', '.env')
        print("Created .env file from template. Please update with your settings.")
    
    # Create necessary directories
    for directory in ['logs', 'notebooks']:
        if not os.path.exists(directory):
            os.makedirs(directory)
            print(f"Created {directory} directory")
    
    # Check if venv exists, create if not
    if not os.path.exists('venv'):
        print("Creating virtual environment...")
        subprocess.run(['python', '-m', 'venv', 'venv'])
        
        # Determine the pip path based on OS
        pip_path = 'venv/bin/pip' if os.name != 'nt' else 'venv\\Scripts\\pip'
        
        # Install dependencies
        print("Installing dependencies...")
        subprocess.run([pip_path, 'install', '-r', 'requirements.txt'])
    
    print("\nSetup complete!")
    print("\nTo run the application:")
    if os.name != 'nt':
        print("1. source venv/bin/activate")
        print("2. flask run")
    else:
        print("1. venv\\Scripts\\activate")
        print("2. flask run")

if __name__ == '__main__':
    setup_environment()
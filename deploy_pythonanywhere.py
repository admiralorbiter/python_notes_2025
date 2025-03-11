#!/usr/bin/env python
"""
Deployment helper script for PythonAnywhere
This script helps with deploying and updating the application on PythonAnywhere.
Run this script from your PythonAnywhere bash console.
"""

import os
import subprocess
import sys

def run_command(command):
    """Run a shell command and print output."""
    print(f"Running: {command}")
    process = subprocess.run(command, shell=True)
    if process.returncode != 0:
        print(f"Command failed with exit code {process.returncode}")
        return False
    return True

def deploy():
    """Run deployment steps for PythonAnywhere."""
    print("="*50)
    print("Python Notes Website - PythonAnywhere Deployment")
    print("="*50)
    
    # 1. Check if we're on PythonAnywhere
    if not os.path.exists('/home/pythonanywhere'):
        print("This script should be run on PythonAnywhere servers.")
        sys.exit(1)
    
    # 2. Ensure we're in the project directory
    project_dir = os.getcwd()
    if not os.path.exists(os.path.join(project_dir, 'wsgi.py')):
        print("Please run this script from the project root directory")
        sys.exit(1)
    
    # 3. Update from git if it's a git repository
    if os.path.exists('.git'):
        print("\n>> Updating code from git repository")
        if not run_command('git pull'):
            choice = input("Git pull failed. Continue anyway? (y/n): ")
            if choice.lower() != 'y':
                sys.exit(1)
    
    # 4. Setup/update virtual environment
    print("\n>> Setting up virtual environment")
    venv_dir = os.path.join(project_dir, 'venv')
    
    if not os.path.exists(venv_dir):
        print("Creating virtual environment...")
        if not run_command('python -m venv venv'):
            print("Failed to create virtual environment")
            sys.exit(1)
    
    # 5. Install/update dependencies
    print("\n>> Installing dependencies")
    if not run_command('venv/bin/pip install -r requirements.txt'):
        print("Failed to install dependencies")
        sys.exit(1)
    
    # 6. Create necessary directories
    print("\n>> Creating necessary directories")
    for directory in ['logs', 'notebooks']:
        if not os.path.exists(directory):
            os.makedirs(directory)
            print(f"Created {directory} directory")
    
    # 7. Create .env file if needed
    if not os.path.exists('.env'):
        print("\n>> Creating .env file")
        if os.path.exists('.env.example'):
            with open('.env.example', 'r') as example_file:
                with open('.env', 'w') as env_file:
                    for line in example_file:
                        if line.startswith('FLASK_ENV='):
                            env_file.write('FLASK_ENV=production\n')
                        elif line.startswith('DEBUG='):
                            env_file.write('DEBUG=False\n')
                        elif line.startswith('SECRET_KEY='):
                            # Generate a random secret key
                            import secrets
                            secret_key = secrets.token_hex(16)
                            env_file.write(f'SECRET_KEY={secret_key}\n')
                        else:
                            env_file.write(line)
            print("Created .env file with production settings")
        else:
            print("Warning: .env.example not found. You need to create .env manually.")
    
    # 8. Reload PythonAnywhere web app
    print("\n>> Reloading PythonAnywhere web app")
    if not run_command('touch /var/www/$(whoami)_pythonanywhere_com_wsgi.py'):
        print("Note: Failed to touch WSGI file. You may need to reload the web app manually.")
    
    print("\n>> Deployment completed successfully!")
    print("\nYour app should now be updated. If you need to configure a web app:")
    print("1. Go to the Web tab in PythonAnywhere dashboard")
    print("2. Add a new web app or modify existing one")
    print(f"3. Set the Source code directory to: {project_dir}")
    print(f"4. Set the Working directory to: {project_dir}")
    print("5. Set the WSGI configuration file to point to: wsgi.py")
    print(f"6. Set the virtualenv path to: {venv_dir}")

if __name__ == '__main__':
    deploy()
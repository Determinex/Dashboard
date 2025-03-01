# dashboard/run.py acts as a vital orchestration tool for automating the setup and management of the Flask application environment.

import os
import sys
import platform
import subprocess
import logging

# Set up logging
log_directory = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'logs')
if not os.path.exists(log_directory):
    os.makedirs(log_directory)

logging.basicConfig(
    filename=os.path.join(log_directory, 'run.log'),
    level=logging.DEBUG,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

def clean():
    """Remove the database and virtual environment."""
    db_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'database', 'dashboard.db')
    env_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'env', platform.system().lower())

    if os.path.exists(db_path):
        os.remove(db_path)
        logging.info(f"Removed database file: {db_path}")
    
    if os.path.exists(env_dir):
        import shutil
        shutil.rmtree(env_dir)
        logging.info(f"Removed virtual environment folder: {env_dir}")
    else:
        logging.warning("Environment folder does not exist.")

def setup():
    """Create a new virtual environment and install dependencies."""
    env_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'env', platform.system().lower())
    venv_path = os.path.join(env_dir, 'venv')

    subprocess.run(['py', '-m', 'venv', venv_path])
    logging.info(f"Created virtual environment: {venv_path}")

    # Activate and upgrade pip
    activate_script = os.path.join(venv_path, 'Scripts', 'activate.bat') if platform.system() == "Windows" else os.path.join(venv_path, 'bin', 'activate')
    subprocess.run(f'CALL {activate_script} && python -m pip install --upgrade pip setuptools wheel', shell=True)

    # Install dependencies
    subprocess.run(f'CALL {activate_script} && python -m pip install -r requirements.txt', shell=True)

def start():
    """Activate the virtual environment and start the Flask application."""
    env_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'env', platform.system().lower())
    venv_path = os.path.join(env_dir, 'venv')
    activate_script = os.path.join(venv_path, 'Scripts', 'activate.bat') if platform.system() == "Windows" else os.path.join(venv_path, 'bin', 'activate')

    # Start the Flask application within the activated virtual environment
    command = f'CALL {activate_script} && flask run --app app.app'
    
    try:
        subprocess.Popen(command, shell=True)
        logging.info("Flask application started.")
    except Exception as e:
        logging.error(f"Failed to start Flask application: {e}")

def list_dependencies():
    """List installed dependencies in the virtual environment."""
    env_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'env', platform.system().lower())
    venv_path = os.path.join(env_dir, 'venv')
    activate_script = os.path.join(venv_path, 'Scripts', 'activate.bat') if platform.system() == "Windows" else os.path.join(venv_path, 'bin', 'activate')

    command = f'CALL {activate_script} && pip list'
    subprocess.run(command, shell=True)

def main():
    """Main function to display menu and execute user choices."""
    while True:
        print("Choose an option:")
        print("1. Clean the database (resetting)")
        print("2. Setup the virtual environment and install dependencies")
        print("3. Start the Flask application")
        print("4. List installed dependencies")
        print("5. Exit")

        choice = input("Enter your choice (1-5): ")
        if choice == "1":
            clean()
        elif choice == "2":
            setup()
        elif choice == "3":
            start()
        elif choice == "4":
            list_dependencies()
        elif choice == "5":
            logging.info("Exiting the application.")
            print("Exiting...")
            sys.exit(0)
        else:
            logging.warning("Invalid choice made by user.")
            print("Invalid choice. Please choose a valid option.")

if __name__ == "__main__":
    logging.info("Application started.")
    main()

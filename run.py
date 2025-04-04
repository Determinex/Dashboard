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

def activate_virtualenv():
    """Activate the virtual environment and return the activation command."""
    env_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'env', platform.system().lower())
    venv_path = os.path.join(env_dir, 'venv')
    if platform.system() == "Windows":
        activate_script = os.path.join(venv_path, 'Scripts', 'activate.bat')
        return f'CALL {activate_script}'
    else:
        activate_script = os.path.join(venv_path, 'bin', 'activate')
        return f'source {activate_script}'

def clean():
    """Remove the database and virtual environment."""
    db_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'database', 'dashboard.db')
    env_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'env', platform.system().lower())

    try:
        if os.path.exists(db_path):
            os.remove(db_path)
            logging.info(f"Removed database file: {db_path}")
        if os.path.exists(env_dir):
            import shutil
            shutil.rmtree(env_dir)
            logging.info(f"Removed virtual environment folder: {env_dir}")
        else:
            logging.warning("Environment folder does not exist.")
    except Exception as e:
        logging.error(f"Error during clean operation: {e}")

def setup():
    """Create a new virtual environment and install dependencies."""
    env_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'env', platform.system().lower())
    venv_path = os.path.join(env_dir, 'venv')
    requirements_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'requirements.txt')

    try:
        subprocess.run(['python', '-m', 'venv', venv_path], check=True)
        logging.info(f"Created virtual environment: {venv_path}")

        # Activate and upgrade pip
        activate_command = activate_virtualenv()
        subprocess.run(f'{activate_command} && python -m pip install --upgrade pip setuptools wheel', shell=True, check=True)

        # Install dependencies
        subprocess.run(f'{activate_command} && python -m pip install -r {requirements_path}', shell=True, check=True)
        logging.info("Installed dependencies from requirements.txt")

    except subprocess.CalledProcessError as e:
        logging.error(f"Error during setup operation: {e}")

def start():
    """Activate the virtual environment and start the Flask application."""
    activate_command = activate_virtualenv()
    possible_app_files = ['app.py', 'application.py', 'main.py']  # List of possible app filenames
    app_file_path = os.path.join(os.path.dirname(os.path.abspath(__file__)))

    # Search for the app file
    for filename in possible_app_files:
        file_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), filename)
        logging.info(f"Checking for Flask application file: {file_path}")
        if os.path.exists(file_path):
            app_file_path = file_path
            logging.info(f"Found Flask application file: {file_path}")
            break
        else:
            logging.warning(f"Flask application file not found: {file_path}")

    if not app_file_path:
        logging.error("No Flask application file found. Searched files: " + ", ".join(possible_app_files))
        return
    
    # Define the configuration dictionary
    config = {
        "host": "127.0.0.1",
        "port": 5000
    }
    config["development"] = {
        "host": "127.0.0.1",
        "port": 5000,
        "debug": True,
        "threaded": True
    }

    # Set the FLASK_APP environment variable
    flask_app_env = f'FLASK_APP={os.path.splitext(os.path.basename(app_file_path))[0]}:app'
    command = f'{activate_command} && set {flask_app_env} && flask run --debugger --reload'

    try:
        process = subprocess.Popen(command, shell=True)
        logging.info("Flask application started.")
        process.wait()
    except KeyboardInterrupt:
        logging.info("Flask application interrupted by user.")
        process.terminate()
    except Exception as e:
        logging.error(f"Failed to start Flask application: {e}")

def list_dependencies():
    """List installed dependencies in the virtual environment."""
    activate_command = activate_virtualenv()
    command = f'{activate_command} && pip list'
    
    try:
        subprocess.run(command, shell=True)
    except Exception as e:
        logging.error(f"Error listing dependencies: {e}")

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
        try:
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
        except Exception as e:
            logging.error(f"Error processing choice {choice}: {e}")

if __name__ == "__main__":
    logging.info("Application started.")
    main()
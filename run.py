# run.py
import os
import sys
import subprocess
import platform
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

def open_terminal_and_run(command):
    """Open a terminal window and run the specified command."""
    logging.info(f"Executing command: {command}")
    try:
        if platform.system() == "Windows":
            subprocess.run(["start", "cmd", "/k", command], shell=True)
        else:  # Assume Linux
            subprocess.run(["gnome-terminal", "--", "bash", "-c", command])
        logging.info(f"Command executed successfully: {command}")
    except Exception as e:
        logging.error(f"Error executing command: {command}. Error: {str(e)}")

def main():
    os_type = platform.system()
    
    # Define the paths for the clean, setup, and start scripts
    if os_type == "Windows": # Adjusted for Windows
        clean_script = "env/windows/clean.bat"
        setup_script = "env/windows/setup.bat"
        start_script = "env/windows/start.bat"
        venv_path = "env/windows/Scripts/activate.bat"  # Adjusted virtual environment path
    else:  # Adjusted for Linux
        clean_script = "env/linux/clean.sh"
        setup_script = "env/linux/setup.sh"
        start_script = "env/linux/start.sh"
        venv_path = "env/linux/venv/bin/activate"  # Adjusted virtual environment path

    # Display menu options
    print("Choose an option:")
    print("1. Clean the database (resetting)")
    print("2. Setup the virtual environment and install dependencies")
    print("3. Start the Flask application")
    print("4. Exit")

    choice = input("Enter your choice (1-4): ")

    if choice == "1":
        command = f"cd env/windows && {clean_script}"  # Ensure the command is correct
        open_terminal_and_run(command)
    elif choice == "2":
        command = f"cd env/windows && {setup_script}"  # Ensure the command is correct
        open_terminal_and_run(command)
    elif choice == "3":
        command = f"cd env/windows && venv\\Scripts\\activate.bat && flask run --debug"  # Ensure the command is correct
        open_terminal_and_run(command)
    elif choice == "4":
        logging.info("Exiting the application.")
        print("Exiting...")
        sys.exit(0)
    else:
        logging.warning("Invalid choice made by user.")
        print("Invalid choice. Please choose a valid option.")

if __name__ == "__main__":
    logging.info("Application started.")
    main()
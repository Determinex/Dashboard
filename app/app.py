# dashboard/app/app.py

from . import create_app  # Import from __init__.py

if __name__ == '__main__':
    app, api = create_app()  # Create the Flask and APIFlask app instances
    app.run(debug=True)  # Start the Flask server

# dashboard/app/app.py

from app import create_app  # Import create_app from the app package

# Run the application
if __name__ == '__main__':
    app, api = create_app()  # Create instances of Flask and APIFlask
    app.run(debug=app.config['DEBUG'])  # Use the DEBUG setting from the configuration
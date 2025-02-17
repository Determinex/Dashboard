from apiflask import APIFlask, Schema
from marshmallow import fields
from src.config import Config # Import your main config file

# ... Your Schema definition ...


def create_app():
    app = APIFlask(__name__, title="My API", version="1.0", docs_path="/docs")
    app.config.from_object(Config) # Load configurations from your config.py
    app.config['SWAGGER_UI_REQUEST_DURATION'] = 1000  #Only APIFlask specific configs here

    # ... your routes and other configurations ...

    return app
from src import create_app
from src.config.config import Config
from dotenv import load_dotenv
import os

# Load environment variables from .env file
env_path = os.path.join(os.path.dirname(__file__), '..', '.env')
print(f"Loading environment variables from: {env_path}")
load_dotenv(env_path)

# Verify environment variables
print(f"SECRET_KEY: {os.getenv('SECRET_KEY')}")
print(f"DATABASE_URL: {os.getenv('DATABASE_URL')}")

# Verify current working directory
print(f"Current working directory: {os.getcwd()}")

app = create_app(Config)

if __name__ == "__main__":
    app.run(debug=True)
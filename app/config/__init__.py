# app/config/__init__.py

from .config import DevConfig, ProdConfig

# Load site settings
site_settings = Config.load_json_settings('app/config/site-settings.json')
user_prefs = Config.load_json_settings('app/config/user-prefs.json')
# settings_manager.py
import configparser
import os

class SettingsManager:
    def __init__(self, settings_file='settings.ini'):
        self.settings_file = settings_file
        self.config = configparser.ConfigParser()
        self.load_settings()

    def load_settings(self):
        if os.path.exists(self.settings_file):
            try:
                self.config.read(self.settings_file)
                self.theme = self.config.get('Appearance', 'theme', fallback='light')
                self.font_size = self.config.getint('Appearance', 'font_size', fallback=12)
                self.background_color = self.config.get('Appearance', 'background_color', fallback='white')
            except Exception as e:
                self.logger.log_error(f"Failed to load settings: {e}")
        else:
            self.theme = 'light'
            self.font_size = 12
            self.background_color = 'white'

    def save_settings(self):
        if 'Appearance' not in self.config:
            self.config['Appearance'] = {}
        self.config['Appearance']['theme'] = self.theme
        self.config['Appearance']['font_size'] = str(self.font_size)
        self.config['Appearance']['background_color'] = self.background_color

        with open(self.settings_file, 'w') as configfile:
            self.config.write(configfile)
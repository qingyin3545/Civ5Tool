import os
import configparser

class ConfigManager:
    def __init__(self, path):
        self.path = path
        self.config = configparser.ConfigParser()

        if os.path.exists(self.path):
            self.config.read(self.path, encoding="utf-8")

    def get(self, section, key, default=None):
        if self.config.has_option(section, key):
            return self.config.get(section, key)
        return default

    def get_int(self, section, key, default=0):
        try:
            return self.config.getint(section, key)
        except Exception:
            return default

    def get_bool(self, section, key, default=False):
        try:
            return self.config.getboolean(section, key)
        except Exception:
            return default

    def set(self, section, key, value):
        if not self.config.has_section(section):
            self.config.add_section(section)
        self.config.set(section, key, str(value))

    def save(self):
        os.makedirs(os.path.dirname(self.path), exist_ok=True) if os.path.dirname(self.path) else None
        with open(self.path, "w", encoding="utf-8") as f:
            self.config.write(f)

config = ConfigManager("Civ5Tool.ini")
import json

from django.conf import settings


class ConfigSettings:
    def __init__(self):
        self.path = settings.LOAD_CONFIG_PATH
        self.data = None

    def load_data(self):
        json_file = open(self.path)
        config_data = json.load(json_file)
        self.data = config_data["data"]
        return True

    def get_all_configs(self, prefix=None):
        self.load_data()
        if prefix:
            return {k: v for k, v in self.data.items() if k.startswith(prefix)}

        return self.data

    def get_conf(self, name):
        self.load_data()
        return self.data.get(name, None)

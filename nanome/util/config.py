import os
import json
from nanome.util import Logs

default_json_string = """{ 
    "host":"127.0.0.1",
    "port":8888,
    "key_file":"nts_key"
}"""

default_json = json.loads(default_json_string)

def _setup_file():
    s = "/"
    
    home = os.getenv('APPDATA')
    if (home == None):
        home = os.getenv('HOME')
    directory = home + s + ".nanome_lib"
    config = directory + s + "config.txt"

    if (not os.path.isdir(directory)):
        try:
            os.mkdir(directory)
        except:
            return False
    if (not os.path.isfile(config)):
        try:
            Logs.message("Creating config file with path " + config_path)
            _setup_clean_config(config)
        except:
            return False
    return config

def _setup_clean_config(config_path):
    with open(config_path, "w") as file:
        file.dump(default_json, file)

def fetch(key):
    if (config_path):
        with open(config_path, "r") as file:
            config_json = json.load(file)
            return config_json[key]
    else:
        return default_json[key]

def set(key, value):
    if (config_path):
        with open(config_path, "r") as file:
            config_json = json.load(file)
            config_json[key] = value
        with open(config_path, "w") as file:
            json.dump(config_json, file)
            return True
    return False

config_path = _setup_file()

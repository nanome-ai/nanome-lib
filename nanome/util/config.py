import os
import json
from nanome.util import Logs

default_json_string = """{
    "host":"127.0.0.1",
    "port":8888,
    "key":"nts_key",
    "plugin_files_path":"~/Documents/nanome-plugins",
    "write_log_file":true
}"""

default_json = json.loads(default_json_string)


def _setup_file():
    s = "/"

    home = os.getenv('APPDATA')
    if home is None:
        home = os.getenv('HOME')
    directory = home + s + ".nanome_lib"
    config = directory + s + "config.txt"

    if not os.path.isdir(directory):
        try:
            os.mkdir(directory)
        except:
            return False
    if not os.path.isfile(config):
        try:
            Logs.message("Creating config file with path " + config)
            _setup_clean_config(config)
        except:
            return False
    return config


def _setup_clean_config(config_path):
    with open(config_path, "w") as file:
        json.dump(default_json, file)


def fetch(key):
    """
    | Fetch a configuration entry from your nanome configuration.
    | Built-in keys are:
    |  host - your NTS server address
    |  port - your NTS server port
    |  key - your NTS key file or string
    |  plugin_files_path - where your plugins will store files
    |  write_log_file - if this is True, plugin will write Logs to a local .log file

    :param key: The key of the config value to fetch
    :type key: :class:`str`
    """
    if config_path:
        try:
            with open(config_path, "r") as file:
                config_json = json.load(file)
                return config_json[key]
        except KeyError:
            value = default_json[key]
            set(key, value)
            return value
    else:
        return default_json[key]


def set(key, value):
    """
    | Set a configuration entry in your nanome configuration.
    | Built-in keys are host, port, key and plugin_files_path.
    | Default values are 127.0.0.1, 8888, nts_key and ~/Documents/nanome-plugins

    :param key: The key of the config value to set
    :type key: :class:`str`
    :param value: The value to set the config item to
    :type value: :class:`str`
    """
    if config_path:
        with open(config_path, "r") as file:
            config_json = json.load(file)
            config_json[key] = value
        with open(config_path, "w") as file:
            json.dump(config_json, file)
            return True
    return False


config_path = _setup_file()

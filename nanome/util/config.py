import argparse
import os
import json
from nanome.util import Logs


__all__ = ["fetch", "set", "settings", "get_config_path", "create_parser"]


default_json_string = """{
    "host":"",
    "port":"8888",
    "key":"",
    "plugin_files_path":"~/Documents/nanome-plugins",
    "write_log_file":true
}"""

default_json = json.loads(default_json_string)


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
    # Get cli args
    plugin_settings = load_settings()
    return plugin_settings.get(key)


def settings():
    return load_settings()


def get_config_path():
    s = "/"
    home = os.getenv('APPDATA')
    if home is None:
        home = os.getenv('HOME')
    directory = home + s + ".nanome_lib"
    config_path = directory + s + "config.txt"
    return config_path


def _setup_file():
    config_path = get_config_path()
    directory = os.path.dirname(config_path)

    if not os.path.isdir(directory):
        try:
            os.mkdir(directory)
        except Exception:
            return False
    if not os.path.isfile(config_path):
        try:
            Logs.message("Creating config file with path " + config_path)
            _setup_clean_config(config_path)
        except Exception:
            return False
    return config_path


def _setup_clean_config(config_path):
    with open(config_path, "w") as file:
        json.dump(default_json, file)


def set(key, value):
    """
    | Set a configuration entry in your nanome configuration.
    | Built-in keys are host, port, key and plugin_files_path.

    :param key: The key of the config value to set
    :type key: :class:`str`
    :param value: The value to set the config item to
    :type value: :class:`str`
    """
    config_path = get_config_path()
    with open(config_path, "r") as file:
        config_json = json.load(file)
        config_json[key] = value

    with open(config_path, "w") as file:
        json.dump(config_json, file)
        return True


def _get_environ_dict():
    """Get values set by environment variables."""
    environ_dict = {
        'host': os.environ.get('NTS_HOST'),
        'port': os.environ.get('NTS_PORT'),
        'key': os.environ.get('NTS_KEY'),
        'auto-reload': os.environ.get('PLUGIN_AUTO_RELOAD'),
        'name': os.environ.get('PLUGIN_NAME'),
        'verbose': os.environ.get('PLUGIN_VERBOSE'),
        'write-log-file': os.environ.get('PLUGIN_WRITE_LOG_FILE'),
        'remote-logging': os.environ.get('PLUGIN_REMOTE_LOGGING'),
    }
    # remove any keys that haven't been set.
    environ_dict = {k: v for k, v in environ_dict.items() if v is not None}
    return environ_dict


def _get_cli_args():
    parser = create_parser()
    cli_dict = vars(parser.parse_known_args()[0])
    for k in list(cli_dict.keys()):
        if cli_dict[k] in [None, '']:
            cli_dict.pop(k)
    return cli_dict


def str2bool(v):
    if isinstance(v, bool):
        return v
    if v.lower() in ('yes', 'true', 't', 'y', '1'):
        return True
    elif v.lower() in ('no', 'false', 'f', 'n', '0'):
        return False
    else:
        raise argparse.ArgumentTypeError('Boolean value expected.')


def create_parser():
    """Command Line Interface for Plugins.

    rtype: argsparser: args parser
    """
    parser = argparse.ArgumentParser(description='Starts a Nanome Plugin.')
    parser.add_argument('-a', '--host', help='connects to NTS at the specified IP address')
    parser.add_argument('-p', '--port', type=int, help='connects to NTS at the specified port')
    parser.add_argument('-r', '--auto-reload', action='store_true', help='Restart plugin automatically if a .py or .json file in current directory changes')
    parser.add_argument('-v', '--verbose', action='store_true', help='enable verbose mode, to display Logs.debug')
    parser.add_argument('-n', '--name', help='Name to display for this plugin in Nanome', default='')
    parser.add_argument('-k', '--keyfile', default='', help='Specifies a key file or key string to use to connect to NTS')
    parser.add_argument('-i', '--ignore', help='To use with auto-reload. All paths matching this pattern will be ignored, use commas to specify several. Supports */?/[seq]/[!seq]', default='')
    parser.add_argument('--write-log-file', type=str2bool, help='Enable or disable writing logs to .log file')
    parser.add_argument('--remote-logging', type=str2bool, dest='remote_logging', help='Toggle whether or not logs should be forwarded to NTS.')
    return parser


def load_settings():
    """Load settings from different sources, and combine them by priority.

    Order of priority for settings:
    1) Highest priority are CLI args used at runtime.
    2) Then environment variables.
    3) Finally, fall back on config file.
    """
    config_path = _setup_file()
    with open(config_path, "r") as f:
        config_dict = json.load(f)

    cli_dict = _get_cli_args()
    environ_dict = _get_environ_dict()

    plugin_settings = dict(config_dict)
    plugin_settings.update(environ_dict)
    plugin_settings.update(cli_dict)
    return plugin_settings


plugin_settings = load_settings()

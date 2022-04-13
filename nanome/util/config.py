import argparse
import os
import json
import logging

"""
Plugin Configurations.

Load settings from different sources, and combine them by priority.

Order of priority for settings:
1) Highest priority are CLI args used at runtime.
2) Then environment variables.
3) Finally, fall back on config file setup with `nanome-setup-plugins` command.

Fetchable Settings
host            NTS host or ip address
port            NTS port
key             Specifies a key file or key string to use to connect to NTS
verbose         Enable verbose mode, to display Logs.debug
name            Name to display for this plugin in Nanome
write_log_file  Enable or disable writing logs to .log file
remote_logging  Toggle whether or not logs should be forwarded to NTS.
auto_reload     Restart plugin automatically if a .py or .json file in current directory changes
ignore          To use with auto-reload. All paths matching this pattern will be ignored,
                use commas to specify several. Supports */?/[seq]/[!seq]

Environment Variable settings keys.
NTS_HOST
NTS_PORT
NTS_KEY
PLUGIN_NAME
PLUGIN_VERBOSE
PLUGIN_WRITE_LOG_FILE
PLUGIN_REMOTE_LOGGING
PLUGIN_AUTO_RELOAD
PLUGIN_IGNORE
"""

__all__ = ['load_settings', 'fetch', 'set', 'create_parser']


def str2bool(v):
    """Accept various truthy/falsey values as boolean arguments."""
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
    parser.add_argument('-k', '--keyfile', dest='key', default='', help='Specifies a key file or key string to use to connect to NTS')
    parser.add_argument('-n', '--name', help='Name to display for this plugin in Nanome', default='')
    parser.add_argument('-v', '--verbose', action='store_true', default=None, help='enable verbose mode, to display Logs.debug')
    parser.add_argument('--write-log-file', type=str2bool, default=None, dest='write_log_file', help='Enable or disable writing logs to .log file')
    parser.add_argument('--remote-logging', type=str2bool, default=None, dest='remote_logging', help='Toggle whether or not logs should be forwarded to NTS.')
    parser.add_argument('-r', '--auto-reload', action='store_true', default=None, dest='auto_reload', help='Restart plugin automatically if a .py or .json file in current directory changes')
    parser.add_argument('-i', '--ignore', help='To use with auto-reload. All paths matching this pattern will be ignored, use commas to specify several. Supports */?/[seq]/[!seq]', default='')
    return parser


def load_settings():
    """Load settings from different sources, and combine them by priority.

    Order of priority for settings:
    1) Highest priority are CLI args used at runtime.
    2) Then environment variables.
    3) Finally, fall back on config file.
    """
    config_dict = _get_config_dict()
    cli_dict = _get_cli_args()
    environ_dict = _get_environ_dict()
    plugin_settings = dict(config_dict)
    plugin_settings.update(environ_dict)
    plugin_settings.update(cli_dict)
    return plugin_settings


def fetch(key):
    """
    | Fetch a configuration value
    | Built-in keys are:
    |  host - your NTS server address
    |  port - your NTS server port
    |  key - your NTS key file or string
    |  plugin_files_path - where your plugins will store files
    |  write_log_file - if this is True, plugin will write Logs to a local .log file

    :param key: The key of the config value to fetch
    :type key: :class:`str`
    """
    plugin_settings = load_settings()
    return plugin_settings.get(key)


def set(key, value):
    """
    | Set a configuration entry in your nanome configuration.
    | Built-in keys are host, port, key and plugin_files_path.

    :param key: The key of the config value to set
    :type key: :class:`str`
    :param value: The value to set the config item to
    :type value: :class:`str`
    """
    config_path = _get_config_path()
    with open(config_path, "r") as file:
        config_json = json.load(file)
        config_json[key] = value

    with open(config_path, "w") as file:
        json.dump(config_json, file)
        return True


def _get_config_dict():
    config_path = _setup_file()
    with open(config_path, "r") as f:
        config_dict = json.load(f)
    serialized_dict = _serialize_dict_with_parser(config_dict)
    return serialized_dict


def _get_environ_dict():
    """Get values set by environment variables."""
    environ_dict = {
        'host': os.environ.get('NTS_HOST'),
        'port': os.environ.get('NTS_PORT'),
        'key': os.environ.get('NTS_KEY'),
        'name': os.environ.get('PLUGIN_NAME'),
        'write_log_file': os.environ.get('PLUGIN_WRITE_LOG_FILE'),
        'remote_logging': os.environ.get('PLUGIN_REMOTE_LOGGING'),
        'auto_reload': os.environ.get('PLUGIN_AUTO_RELOAD'),
        'ignore': os.environ.get('PLUGIN_IGNORE'),
    }
    # Only add verbose key if it is explicitly true (its a store_true arg)
    verbose = str2bool(os.environ.get('PLUGIN_VERBOSE', False))
    if verbose:
        environ_dict['verbose'] = verbose
    serialized_dict = _serialize_dict_with_parser(environ_dict)
    return serialized_dict


def _get_cli_args():
    parser = create_parser()
    cli_dict = vars(parser.parse_known_args()[0])
    for k in list(cli_dict.keys()):
        if cli_dict[k] in [None, '']:
            cli_dict.pop(k)
    return cli_dict


def _setup_file():
    config_path = _get_config_path()
    directory = os.path.dirname(config_path)
    logger = logging.getLogger(__name__)

    if not os.path.isdir(directory):
        try:
            os.mkdir(directory)
        except Exception:
            return False
    if not os.path.isfile(config_path):
        try:
            logger.info("Creating config file with path " + config_path)
            _setup_clean_config(config_path)
        except Exception:
            return False
    return config_path


def _get_config_path():
    s = "/"
    home = os.getenv('APPDATA')
    if home is None:
        home = os.getenv('HOME')
    directory = home + s + ".nanome_lib"
    config_path = directory + s + "config.txt"
    return config_path


def _setup_clean_config(config_path):
    default_json = {
        "host": "",
        "port": "8888",
        "key": "",
        "plugin_files_path": "~/Documents/nanome-plugins",
        "write_log_file": True,
    }
    with open(config_path, "w") as file:
        json.dump(default_json, file)


def _serialize_dict_with_parser(args_dict):
    """Use cli parser to format args as correct data types."""
    parser = create_parser()
    for action in parser._actions:
        field_name = action.dest
        if field_name in args_dict and args_dict[field_name] not in [None, '']:
            arg_list = [action.option_strings[0], str(args_dict[field_name])]
            ns, _ = parser.parse_known_args(arg_list)
            args_dict[field_name] = getattr(ns, field_name)
    args_dict = {k: v for k, v in args_dict.items() if v not in [None, '']}
    return args_dict

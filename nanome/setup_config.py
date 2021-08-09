import argparse
import sys

from nanome.util import config, Logs

config_items = [
    {
        'arg_key': '-a',
        'name': 'NTS Address',
        'description': 'Plugin server address',
        'parse_method': None,
        'key': 'host',
    },
    {
        'arg_key': '-p',
        'name': 'NTS Port',
        'description': 'Plugin server port',
        'key': 'port',
    },
    {
        'arg_key': '-k',
        'name': 'Key File',
        'description': 'Plugin authentication key file or string',
        'key': 'key',
    },
    {
        'arg_key': '-f',
        'name': 'Files Path',
        'description': 'Path that can be used by all plugins to write files (e.g: Uploaded files for Web Loader). "~" will expand to User Folder',
        'key': 'plugin_files_path',
    },
    {
        'arg_key': '--write-log-file',
        'name': 'Write Logs',
        'description': 'Enable .log file writing',
        'key': 'write_log_file'
    }
]


def create_parser():
    """Command Line Interface for Plugins.

    rtype: argsparser: args parser
    """
    parser = argparse.ArgumentParser(description='Set global default values for Plugin configs. Run without arguments for interactive mode')
    parser.add_argument('-a', '--host', help='connects to NTS at the specified IP address')
    parser.add_argument('-p', '--port', type=int, help='connects to NTS at the specified port')
    parser.add_argument('-k', '--keyfile', help='Specifies a key file or key string to use to connect to NTS')
    parser.add_argument('--write-log-file', default=False, type=lambda x: (str(x).lower() == 'true'))
    return parser


def interactive_mode():
    Logs.message("Setup utility for Nanome Plugins global configuration. run without arguments for interactive mode.")

    parser = create_parser()
    for conf in config_items:
        Logs.message("==============================")
        Logs.message(conf['name'] + " (" + conf['description'] + ")")
        Logs.message("Current Value:", config.fetch(conf['key']))
        user_input = input("New Value (leave empty if unchanged): ")
        user_input = user_input.strip()
        if user_input == '':
            continue

        # conf_key = conf['key']
        parser.parse_args([conf['arg_key'], user_input])
        config.set(conf['key'], user_input)


def parse_args():
    parser = create_parser()
    arguments = sys.argv[1:]
    args = parser.parse_args(arguments)
    for key in args.__dict__:
        value = getattr(args, key)
        if value is not None:
            print(f'Setting {key} to {value}')
            config.set(key, value)


def main():
    if (len(sys.argv) == 1):
        interactive_mode()
    else:
        parse_args()


if __name__ == "__main__":
    main()

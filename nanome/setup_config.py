import argparse
import sys
from nanome.util import config


def create_parser():
    """Arguments used to set global config values.
    rtype: argsparser: args parser
    """
    parser = argparse.ArgumentParser(
        description=(
            'Set global default values for Plugin configs. '
            'Run without arguments for interactive mode'
        )
    )
    parser.add_argument('-a', '--host', dest='host', help='NTS host or IP')
    parser.add_argument('-p', '--port', type=int, dest='port', help='NTS port')
    parser.add_argument('-k', '--key', dest='key', help='NTS authentication key file or string')
    parser.add_argument(
        '-f', '--files_path',
        dest='plugin_files_path',
        help=(
            'Path that can be used by all plugins to write files '
            '(e.g: Uploaded files for Web Loader). "~" will expand to User Folder'
        )
    )
    parser.add_argument(
        '--write-log-file',
        default=False,
        type=lambda x: (str(x).lower() in ['true', 'yes', '1']),
        help='Enable or disable .log file writing')
    return parser


def interactive_mode():
    """Set config values one by one using input from the user."""
    print('\nSetup global configurations for Nanome Plugins.\n')

    parser = create_parser()
    for argument in parser._actions:
        config_key = argument.dest
        if config_key == 'help':
            continue

        print("==============================")
        print(config_key + " (" + argument.help + ")")
        print("Current Value: {}".format(config.fetch(config_key)))
        user_input = input("New Value (leave empty if unchanged): ")
        user_input = user_input.strip()
        if user_input == '':
            continue
        namespace = parser.parse_args([argument.option_strings[0], user_input])
        config.set(config_key, getattr(namespace, config_key))


def parse_args():
    """Parse command line args and set config values."""
    parser = create_parser()
    arguments = sys.argv[1:]
    args = parser.parse_args(arguments)
    for key, value in args.__dict__.items():
        if value is not None:
            config.set(key, value)


def main():
    if (len(sys.argv) == 1):
        interactive_mode()
    else:
        parse_args()


if __name__ == "__main__":
    main()

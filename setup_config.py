from nanome.util import config, Logs
import sys

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
        'parse_method': int,
        'key': 'port',
    },
    {
        'arg_key': '-k',
        'name': 'Key File',
        'description': 'Plugin authentication key file',
        'parse_method': None,
        'key': 'key_file',
    },
    {
        'arg_key': '-f',
        'name': 'Files Path',
        'description': 'Path that can be used by all plugins to write files (e.g: Uploaded files for Web Loader). "~" will expand to User Folder',
        'parse_method': None,
        'key': 'plugin_files_path',
    }
]

def parse_value(str, parser):
    if parser == None:
        return str
    try:
        return parser(str)
    except:
        Logs.error("Wrong value:", str, "\nExpected:", parser)
        sys.exit(1)

def interactive_mode():
    Logs.message("Setup utility for Nanome Plugins global configuration")
    for i in range(len(config_items)):
        c = config_items[i]
        Logs.message("==============================")
        Logs.message(c['name'] + " (" + c['description'] + ")")
        Logs.message("Current Value:", config.fetch(c['key']))
        str = input("New Value (leave empty if unchanged): ")
        str = str.strip()
        if str == '':
            continue
        value = parse_value(str, c['parse_method'])
        config.set(c['key'], value)

def display_help():
    Logs.message("The following arguments are available for Nanome Plugins global configuration")
    for i in range(len(config_items)):
        c = config_items[i]
        Logs.message(c['arg_key'], c['name'], '-', c['description'])
    Logs.message("\nOr run without arguments for interactive mode")

def parse_args():
    for i in range(1, len(sys.argv)):
        arg = sys.argv[i]
        if arg == '-h' or arg == 'help' or arg == '--help':
            display_help()
            return

    for i in range(1, len(sys.argv), 2):
        c = None
        for j in range(len(config_items)):
            if config_items[j]['arg_key'] == sys.argv[i]:
                c = config_items[j]
                break
        if c == None:
            Logs.error('Unrecognized argument:', sys.argv[i])
            sys.exit(1)

        if i + 1 >= len(sys.argv):
            Logs.error('Wrong number of argument, each option should have a value following it')
            sys.exit(1)

        value = parse_value(sys.argv[i + 1], c['parse_method'])
        config.set(c['key'], value)

def main():
    if (len(sys.argv) == 1):
        interactive_mode()
    else:
        parse_args()

if __name__ == "__main__":
    main()
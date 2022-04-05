import argparse
import datetime
import os
import re
import sys
import zipfile

TEMPLATE_ZIP = os.path.join(os.path.dirname(__file__), 'plugin-template.zip')

parser = argparse.ArgumentParser(description='Create a plugin')
parser.add_argument('folder', help='Name of plugin folder to be created.')


def main():
    args = parser.parse_args()
    path = args.folder

    fields = {
        'name': 'Example Plugin',
        'description': 'A Nanome Plugin',
        'category': 'other',
        'version': '0.1.0',
        'company': 'Nanome'
    }

    try:
        for key, value in fields.items():
            res = input('%s (%s): ' % (key, value))
            fields[key] = res.strip() or value
    except KeyboardInterrupt:
        print('\nplugin init cancelled')
        sys.exit(0)

    name = ' '.join(w.title() if w.islower() else w for w in fields['name'].split())
    fields['name'] = name
    fields['class'] = re.sub(r'\W', '', name)
    fields['command'] = re.sub(r'\s', '-', name.lower())
    fields['year'] = str(datetime.datetime.today().year)

    with zipfile.ZipFile(TEMPLATE_ZIP, 'r') as z:
        z.extractall(path)

    for root, dirs, files in os.walk(path):
        if '.git' in root:
            continue
        for file in files:
            file_path = os.path.join(root, file)
            with open(file_path, 'r', encoding='utf-8', newline='') as f:
                content = f.read()
            for key, value in fields.items():
                content = content.replace('{{%s}}' % key, value)
            with open(file_path, 'w', encoding='utf-8', newline='') as f:
                f.write(content)
            if file_path.endswith('.sh'):
                perm = os.stat(file_path).st_mode
                os.chmod(file_path, perm | 0o111)

    plugin_path = os.path.join(path, 'plugin', fields['class'] + '.py')
    os.rename(os.path.join(path, 'plugin', 'Plugin.py'), plugin_path)


if __name__ == '__main__':
    main()

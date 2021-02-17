import datetime
import os
import re
import sys
import zipfile

TEMPLATE_ZIP = os.path.join(os.path.dirname(__file__), 'plugin-template.zip')

USAGE = '\n' + sys.argv[0].split('/')[-1] + """ <folder>

    <folder> - name of plugin folder to be created
"""

def main():
    if len(sys.argv) != 2:
        print(USAGE)
        sys.exit(1)

    path = sys.argv[1]
    fields = {
        'name': 'Example Plugin',
        'description': 'A Nanome Plugin',
        'category': 'other',
        'version': '0.1.0',
        'company': 'Nanome',
        'author': 'Nanome',
        'email': 'hello@nanome.ai',
        'repo': 'https://github.com/nanome-ai/'
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
    fields['folder'] = 'nanome_' + re.sub(r'\s', '_', name.lower())
    fields['command'] = fields['folder'].replace('_', '-')
    fields['year'] = str(datetime.datetime.today().year)

    with zipfile.ZipFile(TEMPLATE_ZIP, 'r') as z:
        z.extractall(path)

    for root, dirs, files in os.walk(path):
        if '.git' in root: continue
        for file in files:
            file_path = os.path.join(root, file)
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
            for key, value in fields.items():
                content = content.replace('{{%s}}' % key, value)
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(content)
            if file_path.endswith('.sh'):
                perm = os.stat(file_path).st_mode
                os.chmod(file_path, perm | 0o111)

    plugin_path = os.path.join(path, 'nanome_plugin', fields['class'] + '.py')
    os.rename(os.path.join(path, 'nanome_plugin/Plugin.py'), plugin_path)
    folder_path = os.path.join(path, fields['folder'])
    os.rename(os.path.join(path, 'nanome_plugin'), folder_path)

if __name__ == '__main__':
    main()

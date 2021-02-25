import nanome
from nanome.util import Logs

class {{class}}(nanome.PluginInstance):
    def start(self):
        menu = self.menu
        menu.title = '{{name}}'
        menu.width = 1
        menu.height = 1

        node = menu.root.create_child_node()
        node.add_new_label('hello, nanome!')

    def on_run(self):
        self.menu.enabled = True
        self.update_menu(self.menu)

def main():
    plugin = nanome.Plugin('{{name}}', '{{description}}', '{{category}}', False)
    plugin.set_plugin_class({{class}})
    plugin.run(nanome.config.fetch('host'), nanome.config.fetch('port'))

if __name__ == '__main__':
    main()

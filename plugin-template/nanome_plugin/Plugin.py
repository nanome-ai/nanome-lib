import nanome
from nanome.api.ui import Menu
from nanome.util import Logs


class {{class}}(nanome.PluginInstance):
    def start(self):
        self.menu = Menu()
        self.menu.title = '{{name}}'
        self.menu.width = 1
        self.menu.height = 1

        msg = 'Hello Nanome!'
        node = self.menu.root.create_child_node()
        node.add_new_label(msg)
        Logs.message(msg)


    def on_run(self):
        self.menu.enabled = True
        self.update_menu(self.menu)

def main():
    plugin = nanome.Plugin('{{name}}', '{{description}}', '{{category}}', False)
    plugin.set_plugin_class({{class}})
    plugin.run()


if __name__ == '__main__':
    main()

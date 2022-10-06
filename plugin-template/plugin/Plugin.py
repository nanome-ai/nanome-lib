import nanome
from nanome.api.ui import Menu
from nanome.util import async_callback, Logs


class {{class}}(nanome.AsyncPluginInstance):

    def start(self):
        self.menu = Menu()
        self.menu.title = '{{name}}'
        self.menu.width = 1
        self.menu.height = 1

        msg = 'Hello Nanome!'
        node = self.menu.root.create_child_node()
        self.label = node.add_new_label(msg)
        Logs.message(msg)

    @async_callback
    async def on_run(self):
        # Print the number of complexes in the workspace
        # in the Menu.
        comps = await self.request_complex_list()
        msg = f'{len(comps)} Complex(es) in Workspace'
        Logs.message(msg)
        self.label.text_value = msg
        self.menu.enabled = True
        self.update_menu(self.menu)


def main():
    plugin = nanome.Plugin('{{name}}', '{{description}}', '{{category}}', False)
    plugin.set_plugin_class({{class}})
    plugin.run()


if __name__ == '__main__':
    main()

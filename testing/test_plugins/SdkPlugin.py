import asyncio
import os
from nanome.beta.nanome_sdk import PluginServer, NanomePlugin
from nanome.util import Logs
from nanome.api import ui

class VNMPlugin(NanomePlugin):

    async def on_start(self):
        self.menu = ui.Menu()
        btn = self.menu.root.add_new_button("Save Molecule to DB")
        Logs.message(f"Button: {btn._content_id}")
        self.ui_manager.register_btn_pressed_callback(btn, self.save_mol_to_db)
        self.menu.enabled = True
        self.client.update_menu(self.menu)

    async def save_mol_to_db(self):
        Logs.message("Saved to DB!")


def main():
    server = PluginServer()
    host = os.environ['NTS_HOST']
    port = int(os.environ['NTS_PORT'])
    name = "VNM Test"
    description = "Nanome plugin to load Cryo-EM maps and display them in Nanome as iso-surfaces"
    plugin_class = VNMPlugin
    asyncio.run(server.run(host, port, name, description, plugin_class))


if __name__ == "__main__":
    main()
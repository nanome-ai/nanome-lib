import asyncio
import os
from nanome.beta.nanome_sdk import PluginServer, NanomePlugin
from nanome.util import Logs


class SDKPlugin(NanomePlugin):
    """Test basic plugin using the Nanome SDK."""

    async def on_start(self):
        self.menu = self.ui_manager.create_new_menu()
        btn = self.menu.root.add_new_button("Save Molecule to DB")
        Logs.message(f"Button: {btn._content_id}")
        self.ui_manager.register_btn_pressed_callback(btn, self.save_mol_to_db)
        self.menu.enabled = True
        self.client.update_menu(self.menu)

    async def save_mol_to_db(self, btn):
        Logs.message("Saved to DB!")


if __name__ == "__main__":
    server = PluginServer()
    host = os.environ['NTS_HOST']
    port = int(os.environ['NTS_PORT'])
    name = "SDK Test"
    description = "Test the nanome sdk"
    plugin_class = SDKPlugin
    asyncio.run(server.run(host, port, name, description, plugin_class))

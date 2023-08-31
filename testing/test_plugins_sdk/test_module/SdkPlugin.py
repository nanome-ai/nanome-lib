from nanome.beta.nanome_sdk import NanomePlugin

from .utils import create_menu


class SDKPlugin(NanomePlugin):
    """Test basic plugin using the Nanome SDK."""

    async def on_start(self):
        self.menu = create_menu(self.client)
        self.client.update_menu(self.menu)

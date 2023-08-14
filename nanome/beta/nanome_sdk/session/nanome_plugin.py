from .session_client import SessionClient
from .ui_manager import UIManager


class NanomePlugin:
    """Used as parent class for all Nanome plugins.
    Provides attributes to class instances that inherit from it.

    self.client: SessionClient for sending/receiving messages to/from Nanome
    self.ui_manager: UIManager for creating and managing UI elements and callbacks
    """
    client = None
    ui_manager = UIManager()

    def set_client(self, plugin_id, session_id, version_table):
        """Used internally by the PluginServer."""
        self.client = SessionClient(plugin_id, session_id, version_table)

    async def on_start(self):
        pass

    async def on_stop(self):
        pass

    async def on_complex_added_removed(self):
        pass

import nanome
from nanome.util import Logs
import sys
import time

# Config

NAME = "Sand Box"
DESCRIPTION = "A plugin that can be edited freely for testing."
CATEGORY = "Simple Actions"
HAS_ADVANCED_OPTIONS = False

# Plugin

class SandBox(nanome.PluginInstance):
    def start(self):
        self.request_presenter_info(self.received)
        self.send_notification(nanome.util.enums.NotificationTypes.message, "A" + "\u0394" + "A")

    def on_presenter_change(self):
        self.request_presenter_info(self.received)

    def received(self, presenter_info):
        Logs.message("Presenter:", presenter_info.account_id, presenter_info.account_name, presenter_info.account_email)

    def on_run(self):
        self.request_workspace(self.zoom)

    def zoom(self, workspace):
        for complex in workspace.complexes:
            self.zoom_on_structures(complex)

    def done(self):
        Logs.message("zoom done")

    def __init__(self):
        pass

nanome.Plugin.setup(NAME, DESCRIPTION, CATEGORY, HAS_ADVANCED_OPTIONS, SandBox)
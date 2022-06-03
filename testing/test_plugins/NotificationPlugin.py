import nanome
import sys
import os

from nanome.util import Logs
from nanome.api.structure import Complex, Workspace

# Config

NAME = "Notification Plugin"
DESCRIPTION = "Sends a notification"
CATEGORY = "Test"
HAS_ADVANCED_OPTIONS = False

# Plugin


class NotificationPlugin(nanome.PluginInstance):

    def start(self):
        print("Start Notification Plugin")

    count = 0

    def on_run(self):
        if (NotificationPlugin.count == 0):
            self.send_notification(nanome.util.enums.NotificationTypes.warning, "Warning")
        elif (NotificationPlugin.count == 1):
            self.send_notification(nanome.util.enums.NotificationTypes.error, "Error")
        elif (NotificationPlugin.count == 2):
            self.send_notification(nanome.util.enums.NotificationTypes.message, "Message")
        elif (NotificationPlugin.count == 3):
            self.send_notification(nanome.util.enums.NotificationTypes.success, "success")

        NotificationPlugin.count += 1
        if (NotificationPlugin.count > 3):
            NotificationPlugin.count = 0


nanome.Plugin.setup(NAME, DESCRIPTION, CATEGORY, HAS_ADVANCED_OPTIONS, NotificationPlugin)

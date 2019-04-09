import nanome
import sys
import os

from nanome.util import Logs
from nanome.api.structure import Complex, Workspace


class NotificationPlugin(nanome.PluginInstance):

    def start(self):
        print("Start Notification Plugin")

    count = 0
    def on_run(self):
        if (NotificationPlugin.count == 0):
            self.send_notification(nanome.util.NotificationTypes.warning, "Warning")
        elif (NotificationPlugin.count == 1):
            self.send_notification(nanome.util.NotificationTypes.error, "Error")
        elif (NotificationPlugin.count == 2):
            self.send_notification(nanome.util.NotificationTypes.message, "Message")
        elif (NotificationPlugin.count == 3):
            self.send_notification(nanome.util.NotificationTypes.success, "success")
        
        NotificationPlugin.count += 1
        if (NotificationPlugin.count > 3):
            NotificationPlugin.count = 0

if __name__ == "__main__":
    plugin = nanome.Plugin("Notification Plugin", "sends a notification", "Test", False)
    plugin.set_plugin_class(NotificationPlugin)
    plugin.run('127.0.0.1', 8888)
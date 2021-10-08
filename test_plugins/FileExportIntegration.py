import nanome
from nanome.util import Logs
import sys

# Config

NAME = "File export"
DESCRIPTION = "Test for File Export Integration"
CATEGORY = "File Management"
HAS_ADVANCED_OPTIONS = False

# Plugin


class FileExportIntegration(nanome.PluginInstance):
    def start(self):
        self.integration.export_file = self.export

    def export(self, request):
        (name, data) = request.get_args()
        with open(name, 'w+b') as f:
            f.write(data)


nanome.Plugin.setup(NAME, DESCRIPTION, CATEGORY, HAS_ADVANCED_OPTIONS, FileExportIntegration)

import nanome
from nanome.util import Logs
import os

# Config

NAME = "Generate Molecule Image"
DESCRIPTION = ""
CATEGORY = "Molecule Image"
HAS_ADVANCED_OPTIONS = False

# Plugin


class GenerateMoleculeImageIntegration(nanome.PluginInstance):
    def start(self):
        self.image_path = os.getcwd() + ("/testing/test_assets/images/")
        self.integration.generate_molecule_image = self.make_image

    def make_image(self, request):
        images = []
        i = 1
        for component in request.get_args()[0]:
            path = self.image_path + str(i) + ".png"
            with open(path, "rb") as f:
                data = f.read()
            images.append(data)
            i = (i % 4) + 1
        Logs.debug("Responding...")
        request.send_response(images)


nanome.Plugin.setup(NAME, DESCRIPTION, CATEGORY, HAS_ADVANCED_OPTIONS, GenerateMoleculeImageIntegration)

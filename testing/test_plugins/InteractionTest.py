import nanome
from nanome.util import Color
from nanome.util.enums import InteractionKind
from nanome.api.interactions.interaction import Interaction
import random

# Config

NAME = "Test Interactions"
DESCRIPTION = "A simple plugin demonstrating how plugin system can be used to extend Nanome capabilities"
CATEGORY = "Simple Actions"
HAS_ADVANCED_OPTIONS = False

# Plugin


class InteractionTest(nanome.PluginInstance):
    def start(self):
        pass

    def iter(self, workspace):
        for complex in workspace.complexes:
            for atom in complex.atoms:
                yield atom

    def on_workspace_received(self, workspace):
        atoms = random.sample(list(self.iter(workspace)), 2)
        interaction = Interaction(InteractionKind.HydrogenBond, [atoms[0].index], [atoms[1].index])
        nanome.util.Logs.debug("Upload interaction")
        interaction.upload()
        nanome.util.Logs.debug("Done")

    def on_interactions_received(self, interactions):
        if len(interactions) > 0:
            nanome.util.Logs.debug("Destroy interactions")
            Interaction.destroy_multiple(interactions)
        nanome.util.Logs.debug("Request workspace")
        self.request_workspace(self.on_workspace_received)

    def on_run(self):
        nanome.util.Logs.debug("Getting interactions")
        Interaction.get(self.on_interactions_received)


nanome.Plugin.setup(NAME, DESCRIPTION, CATEGORY, HAS_ADVANCED_OPTIONS, InteractionTest)

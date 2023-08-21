import nanome
from nanome.util import enums, async_callback, Color, Logs
from nanome.api.interactions.interaction import Interaction
import random

# Config

NAME = "Test Interactions"
DESCRIPTION = "A simple plugin demonstrating how plugin system can be used to extend Nanome capabilities"
CATEGORY = "Simple Actions"
HAS_ADVANCED_OPTIONS = False

# Plugin


class InteractionTest(nanome.AsyncPluginInstance):

    def start(self):
        pass

    @async_callback
    async def on_run(self):
        Logs.debug("Getting interactions")
        interactions = await Interaction.get()
        if len(interactions) > 0:
            Logs.debug("Destroy interactions")
            Interaction.destroy_multiple(interactions)
        Logs.debug("Request workspace")
        workspace = await self.request_workspace()
        # Draw an interaction between two random atoms.
        [atom1, atom2] = random.sample(list(self.iter(workspace)), 2)
        interaction = Interaction(enums.InteractionKind.HydrogenBond, [atom1.index], [atom2.index])
        assert interaction.index == -1
        Logs.debug("Upload interaction")
        await Interaction.upload_multiple([interaction])
        assert interaction.index != -1
        Logs.debug("Done")

    def iter(self, workspace):
        for complex in workspace.complexes:
            for atom in complex.atoms:
                yield atom


nanome.Plugin.setup(NAME, DESCRIPTION, CATEGORY, HAS_ADVANCED_OPTIONS, InteractionTest)

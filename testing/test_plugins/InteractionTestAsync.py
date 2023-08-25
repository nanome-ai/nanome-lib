import asyncio
import nanome
import os
import random
from nanome.util import enums, async_callback, Logs
from nanome.api.structure import Complex, Workspace
from nanome.api.interactions.interaction import Interaction


# Config
NAME = "Test Interactions"
DESCRIPTION = "A simple plugin demonstrating how plugin system can be used to extend Nanome capabilities"
CATEGORY = "Simple Actions"
HAS_ADVANCED_OPTIONS = False


PDBOPTIONS = Complex.io.PDBSaveOptions()
PDBOPTIONS.write_bonds = True

# Plugin
test_pdbs = os.path.join(os.path.dirname(__file__), '..', 'test_assets', 'pdb')

class InteractionTest(nanome.AsyncPluginInstance):

    def start(self):
        # Create fresh workspace and load it into Nanome
        self.pdb_file = os.path.join(test_pdbs, '1tyl.pdb')
        self.complex = Complex.io.from_pdb(path=self.pdb_file)
        self.complex.name = "1tyl"
        self.ligand_res = next(res for res in self.complex.residues if res.name == "TYL")
        self.ligand_atom = next(atom for atom in self.ligand_res.atoms)
        self.pocket_res = next(
            res for res in self.complex.residues
            if res.name == "TYR"
            and res.chain.name == "D"    
        )
        self.pocket_atom = next(atom for atom in self.pocket_res.atoms)
        workspace = Workspace()
        workspace.complexes.append(self.complex)
        self.update_workspace(workspace)
    
    @async_callback
    async def on_run(self):
        await self.test_upload()
        await self.test_upload_multiple()

    async def test_upload_multiple(self):
        interactions = await Interaction.get()
        assert len(interactions) == 0
        interaction1 = Interaction(
            enums.InteractionKind.HydrogenBond,
            [self.pocket_atom.index],
            [self.ligand_atom.index])
        interaction2 = Interaction(
            enums.InteractionKind.Covalent,
            [self.pocket_atom.index],
            [self.ligand_atom.index])
        await Interaction.upload_multiple([interaction1, interaction2])
        interactions = await Interaction.get()
        assert len(interactions) == 2
        Interaction.destroy_multiple([interaction1, interaction2])
        assert len(interactions) == 0
        Logs.message("InteractionTest: test_upload_multiple passed")
    
    async def test_upload(self):
        interactions = await Interaction.get()
        assert len(interactions) == 0
        interaction1 = Interaction(
            enums.InteractionKind.HydrogenBond,
            [self.pocket_atom.index],
            [self.ligand_atom.index])
        await interaction1.upload()
        interactions = await Interaction.get()
        assert len(interactions) == 1
        interaction1.destroy()
        
        interactions = Interaction.get()
        assert len(interactions) == 0
        Logs.message("InteractionTest: test_upload passed")

    @async_callback
    async def on_run_old(self):
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

        interaction.visible = False
        interaction.upload()
        self.send_notification(enums.NotificationTypes.message, "Interaction should now be invisible")
        await asyncio.sleep(1)
        interaction.visible = True
        await interaction.upload()
        self.send_notification(enums.NotificationTypes.message, "Interaction should now be visible")
        
        Logs.debug("Done")

    def iter(self, workspace):
        for complex in workspace.complexes:
            for atom in complex.atoms:
                yield atom


nanome.Plugin.setup(NAME, DESCRIPTION, CATEGORY, HAS_ADVANCED_OPTIONS, InteractionTest)

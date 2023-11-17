import asyncio
import sys
import traceback
import nanome
import os
import unittest
from nanome.util import enums, async_callback, Logs
from nanome.api.structure import Complex, Workspace
from nanome.api.interactions import Interaction


# Config
NAME = "[test] Interactions"
DESCRIPTION = "A simple plugin demonstrating how plugin system can be used to extend Nanome capabilities"
CATEGORY = "Simple Actions"
HAS_ADVANCED_OPTIONS = False


PDBOPTIONS = Complex.io.PDBSaveOptions()
PDBOPTIONS.write_bonds = True

# Plugin
test_pdbs = os.path.join(os.path.dirname(__file__), '..', 'test_assets', 'pdb')


class InteractionTest(nanome.AsyncPluginInstance):

    @async_callback
    async def start(self):
        self.starting_ws = await self.request_workspace()

    @async_callback
    async def on_run(self):
        await self.setup_test_workspace()
        await self.run_test_suite()
        # Set original workspace back
        self.update_workspace(self.starting_ws)

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
        interactions = await Interaction.get()
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

        interactions = await Interaction.get()
        assert len(interactions) == 0
        Logs.message("InteractionTest: test_upload passed")

    async def test_toggle_visibility(self):
        interactions = await Interaction.get()
        assert len(interactions) == 0
        interaction = Interaction(
            enums.InteractionKind.HydrogenBond,
            [self.pocket_atom.index],
            [self.ligand_atom.index])
        assert interaction.visible == True
        await interaction.upload()

        # Check that interaction is visible
        interactions = await Interaction.get()
        assert len(interactions) == 1
        interaction = interactions[0]
        assert interaction.visible is True  # This fails.

        interaction.visible = False
        await interaction.upload()
        interactions = await Interaction.get()
        assert len(interactions) == 1
        interaction = interactions[0]
        assert interaction.visible is False  # This fails
        Interaction.destroy_multiple([interaction])

    async def test_filter_by_kind(self):
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

        # Draw another interaction connecting a different atom
        ligand_atom2 = next(atom for atom in self.ligand_res.atoms if atom.index != self.ligand_atom.index)
        interaction3 = Interaction(
            enums.InteractionKind.Covalent,
            [self.pocket_atom.index],
            [ligand_atom2.index])
        await Interaction.upload_multiple([interaction1, interaction2, interaction3])

        interactions = await Interaction.get()
        assert len(interactions) == 3

        covalent_interactions = await Interaction.get(type_filter=enums.InteractionKind.Covalent)
        assert len(covalent_interactions) == 2

        Interaction.destroy_multiple([interaction1, interaction2, interaction3])
        interactions = await Interaction.get()
        assert len(interactions) == 0
        Logs.message("InteractionTest: test_upload_multiple passed")

    async def setup_test_workspace(self):
        """Create fresh workspace and load it into Nanome."""
        self.pdb_file = os.path.join(test_pdbs, '1tyl.pdb')
        workspace = Workspace()
        await self.update_workspace(workspace)
        await self.send_files_to_load(self.pdb_file)
        ws = await self.request_workspace()
        comp = ws.complexes[0]
        assert comp.index != -1
        # Find ligand atom and pocket atom to draw interactions between
        self.ligand_res = next(res for res in comp.residues if res.name == "TYL")
        self.ligand_atom = next(atom for atom in self.ligand_res.atoms)
        self.pocket_res = next(
            res for res in comp.residues
            if res.name == "TYR" and
            res.chain.name == "D"
        )
        self.pocket_atom = next(atom for atom in self.pocket_res.atoms)
        # Make sure test atoms are visible
        for atom in [self.pocket_atom, self.ligand_atom]:
            atom.set_visible(True)
            atom.atom_mode = enums.AtomRenderingMode.Wire
        self.update_structures_shallow([self.pocket_atom, self.ligand_atom])

    async def run_test_suite(self):
        result = unittest.TestResult()
        test_fns = [fn for fn in dir(self) if fn.startswith('test_')]
        for test_fn in test_fns:
            try:
                # Ensure each test starts with interactions cleared.
                interactions = await Interaction.get()
                if interactions:
                    Interaction.destroy_multiple(interactions)
                # Run test
                fn = getattr(self, test_fn)
                await fn()
                result.testsRun += 1
            except Exception as e:
                result.testsRun += 1
                _, _, tb = sys.exc_info()
                result.failures.append((str(test_fn), tb))

        # Display results
        Logs.message("Ran {} tests".format(result.testsRun))
        Logs.message("Failures: {}".format(len(result.failures)))
        Logs.message("Errors: {}".format(len(result.errors)))
        # Display detailed information about test failures
        for test, tb in result.failures + result.errors:
            Logs.message("Test failed: {}".format(test))
            Logs.message(traceback.print_tb(tb))

    async def test_workspace_index_numbering(self):
        ws = await self.request_workspace()
        assert len(ws.complexes) == 1
        comp = ws.complexes[0]
        starting_comp_index = comp.index

        # Add empty workspace
        self.update_workspace(Workspace())
        await self.request_complex_list()

        # Recreate workspace, and we would expect complex index to stay the same
        await self.update_workspace(ws)
        [updated_comp] = await self.request_complex_list()
        assert updated_comp.index != starting_comp_index


nanome.Plugin.setup(NAME, DESCRIPTION, CATEGORY, HAS_ADVANCED_OPTIONS, InteractionTest)

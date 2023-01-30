import json
import os
import sys
import unittest

from nanome.api import macro
from nanome.api.serializers import CommandMessageSerializer
from nanome._internal.network import PluginNetwork
from nanome.api import PluginInstance


if sys.version_info.major >= 3:
    from unittest.mock import MagicMock
else:
    # Python 2.7 way of getting magicmock. Requires pip install mock
    from mock import MagicMock


test_assets = os.getcwd() + ("/testing/test_assets")


class MacroTestCase(unittest.TestCase):

    def setUp(self):
        self.test_macro = """
            --[[

            This macro will cycle through ligands in the workspace and highlight one at a time

            ]]

            function main ()

                ligandResidues = List_Make();

                for complex in List_Iterator(Workspace_GetComplexes()) do
                    molecule = Complex_GetCurrentMolecule(complex);
                    for chain in List_Iterator(Molecule_GetChains(molecule)) do
                        for residue in List_Iterator(Chain_GetResidues(chain)) do
                            if Residue_GetName(residue) ~= "HOH" then
                                containsHetAtoms = false;
                                for atom in List_Iterator(Residue_GetAtoms(residue)) do
                                    containsHetAtoms = Atom_GetIsHet(atom);
                                end;
                                if containsHetAtoms then
                                    List_Add(ligandResidues, residue);
                                end;
                            end;
                        end;
                    end;
                end;

                if List_Length(ligandResidues) <= 0 then
                    return "Error: No ligand found";
                end;

                counter = 0
                if Store_Has("SiteViewMacroCounter") then
                    counter = Store_GetInt("SiteViewMacroCounter");
                end;
                Store_SetInt("SiteViewMacroCounter", counter + 1);

                index = counter % List_Length(ligandResidues);
                ligandResidue = List_Get(ligandResidues, index);

                Selection_Clear();
                Selection_All();

                Command_ShowAtomsBonds(false);
                Command_ShowRibbons(true);
                Command_ShowSurfaces(false);
                Command_ShowWaters(false);
                Command_ShowHydrogens(false);
                Command_ShowAtomLabels(false);
                Command_ShowResidueLabels(false);
                Command_ShowHetAtomsBonds(false);
                Command_ShowHetSurfaces(false);
                Command_SetAtomsBondsRender("default");
                Command_SetRibbonsRender("default");
                Command_SetSurfacesTransparency(0.5);
                Command_ColoringAtomsBonds("chains", nil, nil, true);
                Command_ColoringRibbons("chains");
                Command_ColoringSurfaces("hydrophobicity");
                Selection_Change("replace", ligandResidue);
                Selection_Extend(5.0, true);
                Command_ShowAtomsBonds(true);
                Command_ShowRibbons(true);
                Command_ShowSurfaces(true);
                Command_ShowWaters(true);
                Command_ShowHydrogens(true);
                Command_ShowHetAtomsBonds(true);
                Command_ShowResidueLabels(true);
                Command_SetAtomsBondsRender("wire");
                Selection_Change("filter", ligandResidue);
                Command_SetAtomsBondsRender("sticks");
                Command_ColoringAtomsBonds("default");
                ligandAtomsCount = List_Length(Selection_GetAtoms());
                return "Success: " .. ligandAtomsCount .. " atoms focused";
            end
        """
        version_table_file = os.path.join(test_assets, "version_table_1_24_2.json")
        with open(version_table_file, 'r') as f:
            version_table = json.load(f)

        serializer = CommandMessageSerializer()
        # Mock args that are passed to setup plugin instance networking
        plugin = session_id = queue_in = queue_out = plugin_id = MagicMock()
        self.network = PluginNetwork(plugin, session_id, queue_in, queue_out, serializer, plugin_id, version_table)
        self.macro = macro.Macro(title="test Macro", logic=self.test_macro)

    def test_init(self):
        title = "Test Macro"
        new_macro = macro.Macro(title=title, logic=self.test_macro)
        self.assertEqual(new_macro.title, title)
        self.assertEqual(new_macro.logic, self.test_macro)

    def test_get_plugin_identifier(self):
        # identifier should be 12 random characters
        self.assertEqual(len(self.macro.get_plugin_identifier()), 12)

    def test_run(self):
        PluginNetwork.queue_out = MagicMock()
        PluginInstance._instance = MagicMock()
        PluginInstance._instance.is_async = False
        starting_command_id = PluginNetwork._instance._command_id
        self.macro.run()
        new_command_id = PluginNetwork._instance._command_id
        self.assertEqual(starting_command_id + 1, new_command_id)

    def test_save(self):
        PluginNetwork.queue_out = MagicMock()
        PluginInstance._instance = MagicMock()
        starting_command_id = PluginNetwork._instance._command_id
        PluginInstance._instance.is_async = True
        self.macro.save()
        new_command_id = PluginNetwork._instance._command_id
        self.assertEqual(starting_command_id + 1, new_command_id)

    def test_delete(self):
        PluginNetwork.queue_out = MagicMock()
        all_users = True
        starting_command_id = PluginNetwork._instance._command_id
        self.macro.delete(all_users)
        new_command_id = PluginNetwork._instance._command_id
        self.assertEqual(starting_command_id + 1, new_command_id)

    def test_stop(self):
        PluginNetwork.queue_out = MagicMock()
        starting_command_id = PluginNetwork._instance._command_id
        self.macro.stop()
        new_command_id = PluginNetwork._instance._command_id
        self.assertEqual(starting_command_id + 1, new_command_id)

    def test_get_live(self):
        PluginNetwork.queue_out = MagicMock()
        PluginInstance._instance = MagicMock()
        PluginInstance._instance.is_async = False
        starting_command_id = PluginNetwork._instance._command_id
        self.macro.get_live()
        new_command_id = PluginNetwork._instance._command_id
        self.assertEqual(starting_command_id + 1, new_command_id)

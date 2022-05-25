import os
import unittest
import json

from nanome.api import structure

# Schemas requirements are optional, so don't run tests if they are not installed.
reqs_installed = True
try:
    from nanome.api import schemas
except ModuleNotFoundError:
    reqs_installed = False

test_assets = os.path.join(os.getcwd(), "testing/test_assets")
workspace_json = os.path.join(test_assets, "serialized_data/benzene_workspace.json")
pdb_file = os.path.join(test_assets, "pdb/1tyl.pdb")


@unittest.skipIf(not reqs_installed, "Marshmallow not installed")
class SerializerTestCase(unittest.TestCase):

    def test_load_workspace(self):
        with open(workspace_json, 'r') as f:
            """Deserialize a workspace from JSON."""
            workspace_data = json.load(f)
            workspace = schemas.WorkspaceSchema().load(workspace_data)
            self.assertTrue(isinstance(workspace, structure.Workspace))

    def test_dump_complex(self):
        # Serialize a complex into JSON.
        comp = structure.Complex.io.from_pdb(path=pdb_file)
        self.assertTrue(isinstance(comp, structure.Complex))
        comp_json = schemas.ComplexSchema().dump(comp)
        self.assertTrue(isinstance(comp_json, dict))
        

import json
import nanome
from nanome.util import async_callback, Logs, Color
from nanome.api import schemas, structure

NAME = "Schema Test"
DESCRIPTION = "Tests async/await in plugins."
CATEGORY = "testing"
HAS_ADVANCED_OPTIONS = False


class SchemaBondTest(nanome.AsyncPluginInstance):
    """Validate that bonds aren't lost during schema serialization/deserialization."""

    @async_callback
    async def start(self):
        await self.run_test()

    async def run_test(self):
        shallow = await self.request_complex_list()
        index = shallow[0].index

        [comp] = await self.request_complexes([index])
        atom_count = len(list(comp.atoms))
        bond_count = len(list(comp.bonds))
        comp_data = json.dumps(schemas.ComplexSchema().dump(comp))
        new_comp = schemas.ComplexSchema().loads(comp_data)
        new_comp_atom_count = len(list(new_comp.atoms))
        new_comp_bond_count = len(list(new_comp.bonds))
        assert bond_count == new_comp_bond_count
        assert atom_count == new_comp_atom_count

        for res in new_comp.residues:
            res.ribbon_color = Color.Blue()
        await self.update_structures_deep([new_comp])

        [updated_comp] = await self.request_complexes([index])
        updated_bond_count = len(list(updated_comp.bonds))
        updated_atom_count = len(list(updated_comp.atoms))
        # this assertion fails
        assert bond_count == updated_bond_count
        assert atom_count == updated_atom_count
        Logs.message('done')


nanome.Plugin.setup(NAME, DESCRIPTION, CATEGORY, False, SchemaBondTest)

import os, sys

import nanome
from nanome.util import Logs


NAME = "PDB options only_save_atoms Test"
DESCRIPTION = "Tests only_save_atoms option for the PDB writter."
CATEGORY = "testing"
HAS_ADVANCED_OPTIONS = False

class PDBOnlySaveTest(nanome.PluginInstance):
    def start(self):
        self.on_run()

    def on_run(self):
        # load_url = 'https://files.rcsb.org/download/2kt7.pdb'
        # response = requests.get(load_url)
        # temp = tempfile.NamedTemporaryFile(delete=False)
        # temp.write(response.text.encode("utf-8"))
        # temp.close()
        # complex = nanome.structure.Complex.io.from_pdb(path=temp.name)
        # os.remove(temp.name)

        pdb_path = os.path.join(os.getcwd(), "testing/test_assets/pdb/2kt7.pdb")
        output_path = os.path.join(os.getcwd(), "onlySaveAtomsOutput.pdb")
        complex = nanome.structure.Complex.io.from_pdb(path=pdb_path)
        print('Loaded',pdb_path)

        opts = nanome.util.complex_save_options.PDBSaveOptions()
        opts.only_save_these_atoms = []
        #Pick all atoms but the HIS residues
        for a in complex.atoms:
        	if not a.residue.name == "HIS":
        		opts.only_save_these_atoms.append(a)
        assert(len(opts.only_save_these_atoms) == 1450)
        complex.io.to_pdb(output_path, opts)
        print('Wrote to', output_path)

        complex_verif = nanome.structure.Complex.io.from_pdb(path=output_path)
        assert(len(list(complex_verif.atoms)) == 1450)

        print("Verification complete !")


nanome.Plugin.setup(NAME, DESCRIPTION, CATEGORY, False, PDBOnlySaveTest)
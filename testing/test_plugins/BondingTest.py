import os
import requests
import tempfile

import nanome
from nanome.util import Logs
import sys
import time

NAME = "Bonding Test"
DESCRIPTION = "Tests add_bonds."
CATEGORY = "testing"
HAS_ADVANCED_OPTIONS = False


class BondingTest(nanome.PluginInstance):
    def start(self):
        self.on_run()

    def on_run(self):
        # load_url = 'https://files.rcsb.org/download/1tyl.pdb'
        # response = requests.get(load_url)
        # temp = tempfile.NamedTemporaryFile(delete=False)
        # temp.write(response.text.encode("utf-8"))
        # temp.close()
        # complex = nanome.structure.Complex.io.from_pdb(path=temp.name)
        # os.remove(temp.name)

        pdb_path = os.path.join(os.getcwd(), "testing/test_assets/pdb/1tyl.pdb")
        complex = nanome.structure.Complex.io.from_pdb(path=pdb_path)

        def bonding_done(complex_list):
            self.add_to_workspace(complex_list)
            print('done')

        self.add_bonds([complex], bonding_done)
        print('starting bonding')


nanome.Plugin.setup(NAME, DESCRIPTION, CATEGORY, False, BondingTest)

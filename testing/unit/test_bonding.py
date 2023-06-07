import asyncio
import nanome
import unittest
from nanome._internal.process import Bonding
from nanome.api import structure
import os
from unittest.mock import MagicMock

test_assets = os.getcwd() + ("/testing/test_assets")


def run_awaitable(awaitable, *args, **kwargs):
    loop = asyncio.get_event_loop()
    if loop.is_running:
        loop = asyncio.new_event_loop()
    loop.run_until_complete(awaitable(*args, **kwargs))
    loop.close()


class BondingTestCase(unittest.TestCase):

    def setUp(self):
        nanome.PluginInstance._instance = MagicMock()

    def test_bonding(self):
        pdb_file = os.path.join(test_assets, 'pdb', '3mcf.pdb')
        comp = structure.Complex.io.from_pdb(path=pdb_file)
        bond_count = sum(1 for _ in comp.bonds)
        self.assertEqual(bond_count, 0)

        complex_list = [comp]
        callback = None
        fast_mode = False
        plugin = MagicMock()
        bonding = Bonding(plugin, complex_list, callback, fast_mode)
        bonding.start()

        bond_count = sum(1 for _ in comp.bonds)
        self.assertGreater(bond_count, 0)

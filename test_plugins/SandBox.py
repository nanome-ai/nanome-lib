import os
import nanome
from nanome.api import structure as struct
from nanome.util import Logs
import sys
import time

# Config

NAME = "Sand Box"
DESCRIPTION = "A plugin that can be edited freely for testing."
CATEGORY = "Simple Actions"
HAS_ADVANCED_OPTIONS = False

# Plugin


class SandBox(nanome.PluginInstance):
    def start(self):
        test_assets = os.getcwd() + ("/testing/test_assets")
        filename = test_assets + ("/sdf/small_thrombin.sdf")
        self.complex1 = struct.Complex.io.from_sdf(path=filename)
        self.complex1.name = "complex1"
        self.complex2 = struct.Complex.io.from_sdf(path=filename)
        self.complex2.name = "complex2"
        self.complex3 = struct.Complex.io.from_sdf(path=filename)
        self.complex3.name = "complex3"

    def received(self, presenter_info):
        Logs.message("Presenter:", presenter_info.account_id,
                     presenter_info.account_name, presenter_info.account_email)

    def on_run(self):
        l = [self.complex1, self.complex2, self.complex3]
        self.add_to_workspace(l, self.round_2)

    def round_2(self, complexes):
        Logs.message("round2")
        complexes[0].name = "c1"
        complexes[1].name = "c2"
        complexes[2].name = "c3"
        self.add_to_workspace(complexes)


def __init__(self):
        pass


nanome.Plugin.setup(NAME, DESCRIPTION, CATEGORY, HAS_ADVANCED_OPTIONS, SandBox)

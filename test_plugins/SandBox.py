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
        self.complex2 = struct.Complex.io.from_sdf(path=filename)
        self.complex3 = struct.Complex.io.from_sdf(path=filename)

    def received(self, presenter_info):
        Logs.message("Presenter:", presenter_info.account_id, presenter_info.account_name, presenter_info.account_email)

    def on_run(self):
        l = [self.complex1, self.complex2, self.complex3]
        self.add_to_workspace(l)

    def round_2(self, complexes):
        self.add_to_workspace(complexes)

    def __init__(self):
        pass

nanome.Plugin.setup(NAME, DESCRIPTION, CATEGORY, HAS_ADVANCED_OPTIONS, SandBox)
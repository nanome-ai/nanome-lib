import nanome
from nanome.util import Logs
import test_plugins.fuzzer_helpers as helper
import sys
import random
import time
import testing

# Config

NAME = "Fuzzer"
DESCRIPTION = "A plugin for testing by performing random operations."
CATEGORY = "Simple Actions"
HAS_ADVANCED_OPTIONS = False

class FuzzerInfo(object):
    def __init__(self):
        self.complex_count = 0

class Fuzzer(nanome.PluginInstance):
    def __init__(self):
        nanome._internal._plugin_instance.UPDATE_RATE = .01
        self.fuzzer_info = FuzzerInfo()
        self.running_command = None

    valid_commands = [
        helper.AddSDF,
        helper.AddPDB,
        helper.AddCIF,
        helper.RemoveComplex,
        helper.PrintWorkspace,
        helper.ToggleBonds,
        helper.ToggleSurface,
        helper.ToggleSurface,
        helper.ToggleSurface,
        helper.ToggleSurface,
        helper.ToggleSurface,
        helper.DuplicateFrame,
        helper.RemoveFrame,
        helper.ChangeFrame,

    ]
    def update(self):
        if self.running_command != None and not self.running_command.get_done():
            return
        Logs.reset_tab()
        self.launch_new_command()

    def launch_new_command(self):
        command = self.get_new_command()
        passed = self.check_command(command)
        if not passed:
            self.running_command = None
            return
        self.run_command(command)

    def get_new_command(self):
        num = testing.rand_index(Fuzzer.valid_commands)
        return Fuzzer.valid_commands[num](self.fuzzer_info, self)
        
    def check_command(self, command):
        return command.rules()

    def run_command(self, command):
        command.run()
        self.running_command = command

def tabbed_message(*args):
    if (Logs._tab_count > 0):
        tabs = "| " * Logs._tab_count
        Logs._message(tabs, *args)
    else:
        Logs._message(*args)
def inc_tab():
    Logs._tab_count += 1
def dec_tab():
    Logs._tab_count -= 1
def reset_tab():
    Logs._tab_count = 0
Logs._tab_count = 0
Logs._message = Logs.message
Logs.message = tabbed_message
Logs.inc_tab = inc_tab
Logs.dec_tab = dec_tab
Logs.reset_tab = reset_tab

nanome.Plugin.setup(NAME, DESCRIPTION, CATEGORY, HAS_ADVANCED_OPTIONS, Fuzzer)
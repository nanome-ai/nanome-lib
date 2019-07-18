import nanome
from nanome.util import Logs

# Config

NAME = "Stream Test"
DESCRIPTION = "Simple test for streams"
CATEGORY = "Test"
HAS_ADVANCED_OPTIONS = False
NTS_ADDRESS = '127.0.0.1'
NTS_PORT = 8888

# Plugin

class StreamTest(nanome.PluginInstance):
    def __init__(self):
        self.__running = False

    def on_run(self):
        if self.__running == False:
            self.request_workspace(self.on_workspace_received)
        else:
            self.__running = False
            self.__stream.destroy()

    def update_stream(self):
        if self.__running == False:
            return

        for i in range(0, len(self.__positions), 3):
            self.__positions[i] = (self.__positions[i] + 0.1) % 8
        self.__stream.update(self.__positions, self.update_stream)

    def on_workspace_received(self, workspace):
        indices = []
        self.__positions = []
        for complex in workspace.complexes:
            for atom in complex.atoms:
                indices.append(atom.index)
                self.__positions.append(atom.position.x)
                self.__positions.append(atom.position.y)
                self.__positions.append(atom.position.z)
        self.create_stream(indices, self.on_stream_creation)

    def on_stream_creation(self, stream, error):
        self.__stream = stream
        self.__running = True
        self.update_stream()


nanome.Plugin.setup(NAME, DESCRIPTION, CATEGORY, HAS_ADVANCED_OPTIONS, StreamTest)

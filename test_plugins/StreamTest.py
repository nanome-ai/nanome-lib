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
        self.__stream_count = 0
        self.__done_count = 0

    def on_run(self):
        if self.__running == False:
            self.request_workspace(self.on_workspace_received)
        else:
            self.__running = False
            self.__stream.destroy()
            self.__stream_count = 0
            self.__done_count = 0

    def update_streams(self):
        if self.__running == False:
            return

        for i in range(0, len(self.__positions), 3):
            self.__positions[i] = (self.__positions[i] + 0.1) % 35
        for i in range(0, len(self.__colors), 3):
            self.__colors[i] = (self.__colors[i] + 3) % 255
        for i in range(0, len(self.__scales)):
            self.__scales[i] = (self.__scales[i] + 0.1) % 1.5
        self.__position_stream.update(self.__positions, self.on_stream_update_done)
        self.__color_stream.update(self.__colors, self.on_stream_update_done)
        self.__scale_stream.update(self.__scales, self.on_stream_update_done)

    def on_workspace_received(self, workspace):
        indices = []
        self.__positions = []
        self.__colors = []
        self.__scales = []
        i = 0
        for complex in workspace.complexes:
            for atom in complex.atoms:
                indices.append(atom.index)
                self.__positions.append(atom.position.x)
                self.__positions.append(atom.position.y)
                self.__positions.append(atom.position.z)
                self.__colors.append(i % 255)
                self.__colors.append((i + 50) % 255)
                self.__colors.append((i + 100) % 255)
                self.__scales.append((float(i) / 10.0 + 0.2) % 1.5)
                i += 1
                atom.atom_mode = nanome.api.structure.Atom.AtomRenderingMode.Point

        def workspace_ready():
            self.create_atom_stream(indices, nanome.api.streams.Stream.Type.position, self.on_stream_position_creation)
            self.create_atom_stream(indices, nanome.api.streams.Stream.Type.color, self.on_stream_color_creation)
            self.create_atom_stream(indices, nanome.api.streams.Stream.Type.scale, self.on_stream_scale_creation)

        self.update_structures_deep(list(map(lambda complex : complex, workspace.complexes)), workspace_ready)

    def on_stream_update_done(self):
        self.__done_count += 1
        if self.__done_count >= 3:
            self.__done_count = 0
            self.update_streams()

    def on_stream_position_creation(self, stream, error):
        self.__position_stream = stream
        self.on_stream_creation()

    def on_stream_color_creation(self, stream, error):
        self.__color_stream = stream
        self.on_stream_creation()

    def on_stream_scale_creation(self, stream, error):
        self.__scale_stream = stream
        self.on_stream_creation()

    def on_stream_creation(self):
        self.__stream_count += 1
        if self.__stream_count >= 3:
            self.__running = True
            self.update_streams()


nanome.Plugin.setup(NAME, DESCRIPTION, CATEGORY, HAS_ADVANCED_OPTIONS, StreamTest)

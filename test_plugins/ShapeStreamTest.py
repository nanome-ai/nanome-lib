import nanome
from nanome.util import Logs

# Config

NAME = "Shape Stream Test"
DESCRIPTION = "Test for shape streams"
CATEGORY = "Test"
HAS_ADVANCED_OPTIONS = False

# Plugin

class ShapeStreamTest(nanome.PluginInstance):
    def __init__(self):
        self.__running = False
        self.__stream_count = 0
        self.__done_count = 0

    def on_run(self):
        if self.__running == False:
            self.__sphere = self.create_shape(nanome.util.enums.ShapeType.Sphere)
            self.__sphere.radius = 0.5
            self.__sphere.position = nanome.util.Vector3(0, 0, 0)
            self.__sphere.color = nanome.util.Color(255, 0, 0, 255)
            self.__sphere.upload(self.on_shape_created)
        else:
            self.__running = False
            self.__position_stream.destroy()
            self.__color_stream.destroy()
            self.__scale_stream.destroy()
            self.__stream_count = 0
            self.__done_count = 0

    def update_streams(self):
        if self.__running == False:
            return

        for i in range(0, len(self.__positions)):
            self.__positions[i] = str(int(self.__positions[i]) + 1)
        for i in range(0, len(self.__colors), 3):
            self.__colors[i] = (self.__colors[i] + 3) % 255
        for i in range(0, len(self.__scales)):
            self.__scales[i] = (self.__scales[i] + 0.1) % 1.5
        self.__position_stream.update(self.__positions, self.on_stream_update_done)
        self.__color_stream.update(self.__colors, self.on_stream_update_done)
        self.__scale_stream.update(self.__scales, self.on_stream_update_done)

    def on_shape_created(self, success):
        self.__indices = [self.__sphere.index]
        self.__positions = []
        self.__colors = []
        self.__scales = []
        self.__positions.append(0.0)
        self.__positions.append(0.0)
        self.__positions.append(0.0)
        self.__positions.append(0.0)
        self.__positions.append(0.0)
        self.__positions.append(0.0)
        self.__positions.append(0.0)
        self.__colors.append(255)
        self.__colors.append(0)
        self.__colors.append(0)
        self.__scales.append(0.5)

        self.create_writing_stream(self.__indices, nanome.api.streams.Stream.Type.shape_position_rotation, self.on_stream_position_creation)
        self.create_writing_stream(self.__indices, nanome.api.streams.Stream.Type.shape_color, self.on_stream_color_creation)
        self.create_writing_stream(self.__indices, nanome.api.streams.Stream.Type.sphere_shape_radius, self.on_stream_scale_creation)

    def on_stream_update_done(self):
        self.__done_count += 1
        if self.__done_count >= 4:
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

    def on_stream_complex_creation(self, stream, error):
        self.__complex_stream = stream
        self.on_stream_creation()

    def on_stream_creation(self):
        self.__stream_count += 1
        if self.__stream_count >= 3:
            self.__running = True
            self.update_streams()

nanome.Plugin.setup(NAME, DESCRIPTION, CATEGORY, HAS_ADVANCED_OPTIONS, ShapeStreamTest)

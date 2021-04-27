from nanome.util.vector3 import Vector3
import nanome
import nanome.api.shapes as shapes
from nanome.util import Logs

# Config

NAME = "Shape Stream Test"
DESCRIPTION = "Test for shape streams"
CATEGORY = "Test"
HAS_ADVANCED_OPTIONS = False

# Plugin


class ShapeStreamTest(nanome.PluginInstance):
    def __init__(self):
        self.__indices = []
        self.__spheres_indices = []
        self.__positions = []
        self.__colors = []
        self.__scales = []

        self.__shapes = []
        self.__spheres = []
        self.__lines = []
        self.__running = False
        self.__streams_created = False
        self.__stream_count = 0
        self.__done_count = 0

    def on_run(self):
        if self.__running == False:
            self.make_sphere()
            self.make_line()
            self.make_sphere()
            for shape in self.__shapes:
                shape.upload(self.make_callback(shape))
        else:
            self.__running = False
            self.__position_stream.destroy()
            self.__color_stream.destroy()
            self.__scale_stream.destroy()
            self.__streams_created = False
            self.__stream_count = 0
            self.__done_count = 0

    def update(self):
        if not self.__streams_created:
            if len(self.__indices) == 0:
                return
            for shape in self.__shapes:
                if shape.index < 1:
                    return
            self.create_writing_stream(self.__indices, nanome.api.streams.Stream.Type.shape_position, self.on_stream_position_creation)
            self.create_writing_stream(self.__indices, nanome.api.streams.Stream.Type.shape_color, self.on_stream_color_creation)
            self.create_writing_stream(self.__spheres_indices, nanome.api.streams.Stream.Type.sphere_shape_radius, self.on_stream_scale_creation)
            self.__streams_created = True

    def update_streams(self):
        if self.__running == False:
            return

        for i in range(0, len(self.__positions)):
            sign = (i % 2) - 1
            self.__positions[i] = (self.__positions[i] + (sign * 0.2)) % 5.0
        for i in range(0, len(self.__colors)):
            self.__colors[i] = (self.__colors[i] + 3) % 255
        for i in range(0, len(self.__scales)):
            self.__scales[i] = (self.__scales[i] + 0.1) % 1.5
        self.__position_stream.update(self.__positions, self.on_stream_update_done)
        self.__color_stream.update(self.__colors, self.on_stream_update_done)
        self.__scale_stream.update(self.__scales, self.on_stream_update_done)

    def make_callback(self, shape):
        def cb(result):
            self.__indices.append(shape.index)
            if shape is shapes.Line:
                self.__positions.append(0.0)
                self.__positions.append(0.0)
                self.__positions.append(0.0)
                self.__positions.append(0.0)
                self.__positions.append(0.0)
                self.__positions.append(0.0)
            elif shape is shapes.Sphere:
                self.__spheres_indices.append(shape.index)
                self.__scales.append(0.5)
                self.__positions.append(0.0)
                self.__positions.append(0.0)
                self.__positions.append(0.0)
            else:
                self.__positions.append(0.0)
                self.__positions.append(0.0)
                self.__positions.append(0.0)

            self.__colors.append(255)
            self.__colors.append(0)
            self.__colors.append(0)
            self.__colors.append(255)
        return cb

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

    def make_sphere(self):
        sphere = shapes.Sphere()
        sphere.radius = 0.5
        sphere.position = nanome.util.Vector3(0, 0, 0)
        sphere.color = nanome.util.Color(255, 0, 0, 255)
        self.__shapes.append(sphere)
        return sphere

    def make_line(self):
        line = shapes.Line()
        line.anchors[0].position = nanome.util.Vector3(0, 0, 0)
        line.anchors[1].position = nanome.util.Vector3(0, 0, 0)
        line.color = nanome.util.Color(255, 0, 0, 255)
        self.__shapes.append(line)
        return line


nanome.Plugin.setup(NAME, DESCRIPTION, CATEGORY, HAS_ADVANCED_OPTIONS, ShapeStreamTest)

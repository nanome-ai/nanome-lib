from nanome._internal._util._serializers import _TypeSerializer
from nanome._internal._shapes._mesh import _Mesh
from nanome.util import Logs

import tempfile
import os
from io import BytesIO
try:
    from PIL import Image
    pillow_available = True
except ImportError:
    pillow_available = False


class _MeshSerializer(_TypeSerializer):
    def __init__(self):
        pass

    def version(self):
        return 0

    def name(self):
        return "MeshShape"

    def read_texture(self, value):
        if pillow_available and type(value.texture_path) == str:
            path = value.texture_path.replace("\\", "/")
            if os.path.isfile(path):
                try:
                    img = Image.open(path, mode='r')
                    byte_arr = BytesIO()
                    img.save(byte_arr, format='PNG')
                    texture_bytes = byte_arr.getvalue()
                    return (texture_bytes, [img.size[0], img.size[1]])
                except Exception as e:
                    Logs.Error("Error reading texture file: " + e)
            else:
                Logs.Error("Texture file does not exist")
        return ([], [0, 0])

    def create_texture(self, path, size, array):
        img = Image.open(BytesIO(array))
        img.save(path, format='PNG')

    def serialize(self, version, value, context):
        context.write_float_array(value.vertices)
        context.write_float_array(value.normals)
        context.write_float_array(value.colors)
        context.write_int_array(value.triangles)
        context.write_float_array(value.uv)

        texture_bytes, texture_size = self.read_texture(value)
        context.write_int_array(texture_size)
        context.write_byte_array(texture_bytes)
        if texture_size[0] > 0 and texture_size[1] > 0:
            Logs.debug("Sending texture of size", texture_size)

    def deserialize(self, version, context):
        result = _Mesh._create()
        result.vertices = context.read_float_array()
        result.normals = context.read_float_array()
        result.colors = context.read_float_array()
        result.triangles = context.read_int_array()
        result.uv = context.read_float_array()
        texture_size = context.read_int_array()

        if texture_size[0] > 0 and texture_size[1] > 0:
            temp_texture = tempfile.NamedTemporaryFile(delete=False, suffix='png')
            texture_bytes = context.read_byte_array()
            self.create_texture(temp_texture.name, texture_size, texture_bytes)
            result.texture_path = temp_texture.name
        return result

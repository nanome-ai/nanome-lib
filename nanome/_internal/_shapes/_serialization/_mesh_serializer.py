import os
import tempfile

from nanome._internal._shapes._mesh import _Mesh
from nanome._internal._util._serializers import _TypeSerializer
from nanome.util import Logs


class _MeshSerializer(_TypeSerializer):
    def __init__(self):
        pass

    def version(self):
        return 1

    def name(self):
        return "MeshShape"

    def read_texture(self, value):
        if value.texture_path != "":
            filename, ext = os.path.splitext(value.texture_path)
            if ext.lower() in [".jpeg", ".jpg", ".png"]:
                path = value.texture_path.replace("\\", "/")
                if os.path.isfile(path):
                    try:
                        with open(path, "rb") as f:
                            texture_bytes = bytearray(f.read())
                            return texture_bytes
                    except Exception as e:
                        Logs.error("Error reading texture file: " + e)
                else:
                    Logs.error("Texture file does not exist")
            else:
                Logs.error("Texture file should be a png or a jpg file")
        return []

    def serialize(self, version, value, context):
        context.write_float_array(value.vertices)
        context.write_float_array(value.normals)
        context.write_float_array(value.colors)
        context.write_int_array(value.triangles)
        context.write_float_array(value.uv)

        texture_bytes = self.read_texture(value)
        context.write_byte_array(texture_bytes)
        if len(texture_bytes) > 0:
            Logs.debug("Sending texture:", value.texture_path)

        if version >= 1:
            context.write_bool(value.unlit)

    def create_texture_file(self, texture_path, texture_bytes):
        with open(texture_path, "wb") as f:
            f.write(texture_bytes)

    def deserialize(self, version, context):
        result = _Mesh._create()
        result.vertices = context.read_float_array()
        result.normals = context.read_float_array()
        result.colors = context.read_float_array()
        result.triangles = context.read_int_array()
        result.uv = context.read_float_array()
        texture_bytes = context.read_byte_array()

        if version >= 1:
            result.unlit = context.read_bool()

        if len(texture_bytes) > 0:
            temp_texture = tempfile.NamedTemporaryFile(delete=False, suffix='png')
            self.create_texture_file(temp_texture.name, texture_bytes)
            result.texture_path = temp_texture.name
        return result

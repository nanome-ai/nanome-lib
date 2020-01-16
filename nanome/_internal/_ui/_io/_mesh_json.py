from .. import _Mesh
from nanome.util.color import Color

def parse_json(content_json):
    mesh = _Mesh._create()
    mesh._mesh_color = content_json.read("mesh_color", mesh._mesh_color)
    return mesh

def write_json(helper, mesh):
    helper.write("mesh_color", mesh._mesh_color)

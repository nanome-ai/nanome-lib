from .. import _Mesh
from nanome.util.color import Color

def parse_json(content_json):
    mesh = _Mesh._create()
    mesh._mesh_color = Color.from_int(int(float((content_json["mesh_color"]))))
    return mesh

def write_json(mesh):
    content_json = {}
    content_json["mesh_color"] = mesh._mesh_color._color
    return content_json

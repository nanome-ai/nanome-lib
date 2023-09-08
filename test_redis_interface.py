import time
from nanome.beta.redis_interface import PluginInstanceRedisInterface
from nanome.util import enums
from nanome.api import shapes

__all__ = ['test_color_stream']

REDIS_HOST = 'localhost'
REDIS_PORT = 6379
REDIS_PASSWORD = None
REDIS_CHANNEL = '3PCX0'
plugin = PluginInstanceRedisInterface(
    REDIS_HOST, REDIS_PORT, REDIS_PASSWORD, REDIS_CHANNEL)
plugin.connect()

ws = plugin.request_workspace()
comps = ws.complexes
comp = comps[0]
atom_indices = [atm.index for atm in comp.atoms]

def test_shape_uploads(atom_indices):
    sphere = shapes.Sphere()
    sphere.radius = 10.0
    anchor = sphere.anchors[0]
    anchor.anchor_type = enums.ShapeAnchorType.Atom
    anchor.target = atom_indices[0]
    [sphere] = plugin.upload_shapes([sphere])
    for atom_index in atom_indices:
        anchor.target = atom_index
        [sphere] = plugin.upload_shapes([sphere])
        time.sleep(0.01)

def test_color_stream(atom_indices):
    stream_type = enums.StreamType.color
    color_stream = plugin.create_writing_stream(atom_indices, stream_type)
    # RGB values of the rainbow
    roygbiv = [
        (255, 0, 0),  # Red
        (255, 127, 0),  # Orange
        (255, 255, 0),  # Yellow
        (0, 255, 0),  # Green
        (0, 0, 255),  # Blue
        (75, 0, 130),  # Indigo
        (148, 0, 211),  # Violet
    ]
    j = 0
    for _ in range(0, 5):
        stream_data = []
        for atm_index in atom_indices:
            stream_data.extend(roygbiv[j % len(roygbiv)])
            j += 1
        plugin.update_stream(color_stream, stream_data)
    plugin.destroy_stream(color_stream)

    color_scheme = enums.ColorScheme.BFactor
    color_scheme_target = enums.ColorSchemeTarget.All
    plugin.apply_color_scheme(color_scheme, color_scheme_target)
    plugin.center_on_structures([comp])

# test_color_stream(atom_indices)

# import os
# import sys
# breakpoint()
# filedir = os.path.dirname(__file__)
# sys.path.append(filedir)
from nanome.beta.redis_interface import PluginInstanceRedisInterface
from nanome.util import enums, Color

REDIS_HOST = 'localhost'
REDIS_PORT = 6379
REDIS_PASSWORD = None
REDIS_CHANNEL = 'LVPL8'
plugin = PluginInstanceRedisInterface(
    REDIS_HOST, REDIS_PORT, REDIS_PASSWORD, REDIS_CHANNEL)
plugin.connect()
ws = plugin.request_workspace()

comps = ws.complexes
comp = comps[0]

atom_indices = [atm.index for atm in comp.atoms]
stream_type = enums.StreamType.color
stream_id, error, _ = plugin.create_writing_stream(atom_indices, stream_type)[1:]

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

color_rgba = Color.Blue().rgba
stream_data = []
for atm_index in atom_indices:
    stream_data.extend(color_rgba)
breakpoint()
plugin.stream_update(stream_id, stream_data)


color_scheme = enums.ColorScheme.BFactorAF
color_scheme_target = enums.ColorSchemeTarget.All
plugin.apply_color_scheme(color_scheme, color_scheme_target)
plugin.center_on_structures([comp])

import os
import sys

root_path = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.insert(0, root_path)
from nanome.beta.redis_interface import PluginInstanceRedisInterface
REDIS_HOST = 'localhost'
REDIS_PORT = 6379
REDIS_PASSWORD = None
REDIS_CHANNEL = 'LVPL8'
plugin = PluginInstanceRedisInterface(REDIS_HOST, REDIS_PORT, REDIS_PASSWORD, REDIS_CHANNEL)
plugin.connect()
shallow_comps = plugin.request_complex_list()
comp_ids = [comp.index for comp in shallow_comps]
comps = plugin.request_complexes(comp_ids)
for comp in comps:
    assert len(list(comp.atoms)) > 0

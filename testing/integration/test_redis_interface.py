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
plugin.request_complex_list()
pass
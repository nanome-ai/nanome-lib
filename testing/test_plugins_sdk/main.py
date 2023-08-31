import asyncio
import os
from nanome.beta.nanome_sdk import PluginServer, NanomePlugin
import test_module
from test_module.SdkPlugin import SDKPlugin

if __name__ == "__main__":
    server = PluginServer()
    host = os.environ['NTS_HOST']
    port = int(os.environ['NTS_PORT'])
    name = "SDK Test"
    description = "Test the nanome sdk"
    plugin_module = test_module
    plugin_class = test_module.SdkPlugin.SDKPlugin
    asyncio.run(server.run(host, port, name, description, plugin_module, plugin_class))

import nanome
from nanome.util import async_callback, Logs, Process

NAME = "Async Process Test"
DESCRIPTION = "Tests async/await on Process API for plugins."
CATEGORY = "testing"
HAS_ADVANCED_OPTIONS = False


class AsyncTest(nanome.AsyncPluginInstance):
    def start(self):
        self.on_run()

    @async_callback
    async def on_run(self):
        p = Process(label="echo hello world")
        p.executable_path = '/bin/echo'
        p.args = ['hello world']
        p.output_text = True
        p.on_error = Logs.error
        p.on_output = Logs.message
        await p.start()
        # test executing process second time
        await p.start()


nanome.Plugin.setup(NAME, DESCRIPTION, CATEGORY, False, AsyncTest)

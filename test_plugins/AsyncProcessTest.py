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
        exit_code = await p.start()
        assert exit_code == 0, "Process did not return 0"

        # test that timeout works
        proc = Process(label="sleep", timeout=1)
        proc.on_error = Logs.error
        proc.executable_path = '/bin/sleep'
        proc.args = ['2']
        exit_code = await proc.start()
        assert exit_code == -9, f"Process return exit code {exit_code} instead of -9"

        # test executing process second time
        exit_code = await p.start()
        assert exit_code == 0, "Process did not return 0"

nanome.Plugin.setup(NAME, DESCRIPTION, CATEGORY, False, AsyncTest)

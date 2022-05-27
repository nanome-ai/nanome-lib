import nanome
from nanome.util import async_callback, Logs, Process

NAME = "Async Process Test"
DESCRIPTION = "Tests async/await on Process API for plugins."
CATEGORY = "testing"
HAS_ADVANCED_OPTIONS = False


class AsyncProcessTest(nanome.AsyncPluginInstance):

    def start(self):
        self.on_run()

    @async_callback
    async def on_run(self):
        # Test basic process creation
        p = Process(label="echo hello world")
        p.executable_path = '/bin/echo'
        p.args = ['hello world']
        p.output_text = True
        p.on_error = Logs.error
        p.on_output = Logs.message
        exit_code = await p.start()
        expected_code = 0
        assert exit_code == expected_code, f"Process returned {exit_code} instead of {expected_code}"

        # test that timeout works
        proc = Process(label="sleep", timeout=1)
        proc.on_error = Logs.error
        proc.executable_path = '/bin/sleep'
        proc.args = ['2']
        exit_code = await proc.start()
        expected_code = Process.TIMEOUT_CODE
        assert exit_code == expected_code, f"Process returned {exit_code} instead of {expected_code}"


nanome.Plugin.setup(NAME, DESCRIPTION, CATEGORY, False, AsyncProcessTest)

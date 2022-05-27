import nanome
from nanome.util import async_callback, Logs

NAME = "Async Test"
DESCRIPTION = "Tests async/await in plugins."
CATEGORY = "testing"
HAS_ADVANCED_OPTIONS = False


class AsyncTest(nanome.AsyncPluginInstance):
    def start(self):
        self.on_run()

    @async_callback
    async def on_run(self):
        shallow = await self.request_complex_list()
        index = shallow[0].index

        deep = await self.request_complexes([index])
        complex = deep[0]
        complex.position.x += 1

        await self.update_structures_deep([complex])
        Logs.message('done')


nanome.Plugin.setup(NAME, DESCRIPTION, CATEGORY, False, AsyncTest)

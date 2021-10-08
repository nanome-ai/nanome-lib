from nanome.util import Logs

import asyncio
import traceback
from timeit import default_timer as timer


async def _async_update_loop(self, UPDATE_RATE, MINIMUM_SLEEP):
    try:
        self.start()
        last_update = timer()
        while self._network._receive() and self._process_manager.update():
            self.update()

            dt = last_update - timer()
            sleep_time = max(UPDATE_RATE - dt, MINIMUM_SLEEP)
            await asyncio.sleep(sleep_time)
            last_update = timer()

    except KeyboardInterrupt:
        self._on_stop()
        return
    except:
        Logs.error(traceback.format_exc())
        self._on_stop()
        self._process_manager._close()
        self._network._close()
        return

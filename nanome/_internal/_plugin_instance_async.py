from nanome.util import Logs

import asyncio
import traceback
from timeit import default_timer as timer


async def async_update_loop(plugin_instance, UPDATE_RATE, MINIMUM_SLEEP):
    try:
        plugin_instance.start()
        last_update = timer()
        while plugin_instance._network._receive() and plugin_instance._process_manager.update():
            plugin_instance.update()

            dt = last_update - timer()
            sleep_time = max(UPDATE_RATE - dt, MINIMUM_SLEEP)
            await asyncio.sleep(sleep_time)
            last_update = timer()

    except KeyboardInterrupt:
        plugin_instance._on_stop()
        return
    except:
        msg = traceback.format_exc()
        # Print manually because for some reason Logs.error doesn't display it.
        # TODO: Investigate why.
        print(msg)
        Logs.error(msg)
        plugin_instance._on_stop()
        plugin_instance._process_manager._close()
        plugin_instance._network._close()
        return

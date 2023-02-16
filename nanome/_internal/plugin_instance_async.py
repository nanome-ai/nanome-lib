import asyncio
import sys
from timeit import default_timer as timer
import logging

logger = logging.getLogger(__name__)


async def async_update_loop(plugin_instance, UPDATE_RATE, MINIMUM_SLEEP):
    try:
        plugin_instance.start()
        loop_start_time = timer()
        last_update = timer()
        while plugin_instance._network._receive() and plugin_instance._process_manager.update():
            plugin_instance.update()
            dt = last_update - timer()
            sleep_time = max(UPDATE_RATE - dt, MINIMUM_SLEEP)
            await asyncio.sleep(sleep_time)
            last_update = timer()
            if last_update - loop_start_time > plugin_instance._session_timeout:
                raise TimeoutError()

    except KeyboardInterrupt:
        plugin_instance._on_stop()
        return
    except TimeoutError:
        logger.warning("Session timed out")
        plugin_instance._on_stop()
        plugin_instance._process_manager._close()
        plugin_instance._network._close()
        return
    except Exception:
        from nanome.util.asyncio import handle_exception
        await handle_exception(*sys.exc_info())
        plugin_instance._on_stop()
        plugin_instance._process_manager._close()
        plugin_instance._network._close()
        return

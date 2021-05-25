import asyncio


def async_callback(fn):
    def task(*args, **kwargs):
        loop = asyncio.get_running_loop()
        return loop.create_task(fn(*args, **kwargs))
    return task

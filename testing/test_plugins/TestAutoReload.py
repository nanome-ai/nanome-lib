import nanome

from multiprocessing import Process
import time
import sys


def start_process():
    print("Start subproc")
    sys.stdout.flush()
    while True:
        print("Hello")
        sys.stdout.flush()
        time.sleep(3)


class Test(nanome.PluginInstance):
    pass


process = None


def pre_run():
    print("Pre run")
    sys.stdout.flush()
    global process
    process = Process(target=start_process)
    process.start()


def post_run():
    print("Post run")
    sys.stdout.flush()
    process.kill()


if __name__ == "__main__":
    plugin = nanome.Plugin("Test Autoreload", "", "Test", False)
    plugin.pre_run = pre_run
    plugin.post_run = post_run
    plugin.set_plugin_class(Test)
    plugin.run('127.0.0.1', 8888)

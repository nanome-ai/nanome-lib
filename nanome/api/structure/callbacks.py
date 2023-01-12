
def complex_added(network, arg, request_id):
    network.on_complex_added()


def complex_removed(network, arg, request_id):
    network.on_complex_removed()


def complex_updated(network, arg, request_id):
    from nanome.api import PluginInstance
    PluginInstance._on_complex_updated(arg[0], arg[1])


def selection_changed(network, arg, request_id):
    from nanome.api import PluginInstance
    PluginInstance._on_selection_changed(arg[0], arg[1])


def receive_complexes(network, arg, request_id):
    for i in range(len(arg)):
        if arg[i]._index == -1:
            arg[i] = None
    network._call(request_id, arg)

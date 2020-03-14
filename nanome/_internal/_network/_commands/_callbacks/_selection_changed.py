import nanome

def _selection_changed(network, arg, request_id):
    nanome._internal._PluginInstance._on_selection_changed(arg[0], arg[1])
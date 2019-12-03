import nanome

def _complex_updated(network, arg, request_id):
    nanome._internal._PluginInstance._on_complex_updated(arg.index, arg)
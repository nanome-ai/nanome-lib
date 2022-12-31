import nanome


def _complex_updated(network, arg, request_id):
    nanome._internal._PluginInstance._on_complex_updated(arg[0], arg[1])

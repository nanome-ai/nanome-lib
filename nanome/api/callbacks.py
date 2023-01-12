import logging
from ._hashes import Hashes
from nanome.api import PluginInstance

from nanome.api.streams import Stream
from nanome.api.integration import Integration, IntegrationRequest
from nanome.util.stream import StreamCreationError

logger = logging.getLogger(__name__)


def advanced_settings(network, args, request_id):
    network.on_advanced_settings()


def connect(network, arg, request_id):
    pass


def receive_create_stream_result(network, result, request_id):
    if result[0] != StreamCreationError.NoError:
        network._call(request_id, None, result[0])

        if result[0] == StreamCreationError.UnsupportedStream:
            logger.error("Tried to create an unsupported type of stream")
        return

    stream = Stream(network, result[1], result[2], result[3])
    network._call(request_id, stream, StreamCreationError.NoError)


def feed_stream(network, result, request_id):
    Stream._streams[result[0]]._update_received(result[1])


def integration(network, args, request_id):
    integration = network._plugin.integration
    request = IntegrationRequest(args[0], args[1], args[2], network)
    name = Hashes.HashToIntegrationName[args[1]]
    Integration._call(integration, name, request)


def receive_interrupt_stream(network, result, request_id):
    try:
        stream = Stream._streams[result[1]]
    except:
        logger.warning(
            f"Got an error for an unknown stream. Probably tried to update an unknown stream: {result[1]}")
        return

    stream._interrupt(result[0])


def presenter_change(network, arg, request_id):
    network._on_presenter_change()


def run(network, args, request_id):
    network._on_run()


def simple_callback_arg_unpack(network, arg, request_id):
    network._call(request_id, *arg)


def simple_callback_arg(network, arg, request_id):
    network._call(request_id, arg)


def simple_callback_no_arg(network, arg, request_id):
    network._call(request_id)


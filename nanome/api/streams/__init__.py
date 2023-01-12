from . import *
from .stream import Stream
from . import messages, callbacks

from nanome._internal.enums import Commands
from nanome.api import callbacks as base_callbacks

registered_commands = [
    (Commands.stream_create_done, messages.CreateStreamResult(), callbacks.receive_create_stream_result),
    (Commands.stream_feed, messages.FeedStream(), callbacks.feed_stream),
    (Commands.stream_interrupt, messages.InterruptStream(), callbacks.receive_interrupt_stream),
    (Commands.stream_feed_done, messages.FeedStreamDone(), base_callbacks.simple_callback_no_arg),
]
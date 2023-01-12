from .presenter_info import PresenterInfo  # noqa: F401
from . import messages, callbacks

from nanome._internal.enums import Commands
from nanome.api import callbacks as base_callbacks


registered_commands = [
    (Commands.presenter_info_response, messages.GetPresenterInfoResponse(), base_callbacks.simple_callback_arg),
    (Commands.presenter_change, messages.PresenterChange(), callbacks.presenter_change),
]

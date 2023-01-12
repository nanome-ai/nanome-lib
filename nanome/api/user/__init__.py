from .presenter_info import PresenterInfo  # noqa: F401
from . import messages, callbacks

from nanome._internal.enums import Commands, Messages
from nanome.util import simple_callbacks


registered_commands = [
    (Commands.presenter_info_response, messages.GetPresenterInfoResponse(), simple_callbacks.simple_callback_arg),
    (Commands.presenter_change, messages.PresenterChange(), callbacks.presenter_change),
]

registered_messages = [
    (Messages.presenter_info_request, messages.GetPresenterInfo()),
]

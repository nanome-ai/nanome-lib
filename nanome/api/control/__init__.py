from . import messages, callbacks

from nanome.util import simple_callbacks
from nanome._internal.enums import Commands

registered_commands = [
    (Commands.connect, messages.Connect(), callbacks.connect),
    (Commands.run, messages.Run(), callbacks.run),
    (Commands.advanced_settings, messages.AdvancedSettings(), callbacks.advanced_settings),
    (Commands.controller_transforms_response, messages.GetControllerTransformsResponse(), simple_callbacks.simple_callback_arg_unpack),
]
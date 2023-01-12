from .macro import Macro  # noqa: F401
from . import serializers, messages  # noqa: F401

from nanome._internal.enums import Commands
from nanome.api import callbacks as base_callbacks

registered_commands = [
    (Commands.get_macros_response, messages.GetMacrosResponse(), base_callbacks.simple_callback_arg),
    (Commands.run_macro_result, messages.RunMacro(), base_callbacks.simple_callback_arg),
]
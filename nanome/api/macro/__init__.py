from .macro import Macro  # noqa: F401
from . import serializers, messages  # noqa: F401

from nanome._internal.enums import Commands
from nanome.util import simple_callbacks 

registered_commands = [
    (Commands.get_macros_response, messages.GetMacrosResponse(), simple_callbacks.simple_callback_arg),
    (Commands.run_macro_result, messages.RunMacro(), simple_callbacks.simple_callback_arg),
]
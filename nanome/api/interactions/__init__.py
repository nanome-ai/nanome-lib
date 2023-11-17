from . import *
from nanome._internal.enums import Commands, Messages
from nanome.util import simple_callbacks
from .interaction import Interaction  # noqa: F401
from . import serializers, messages  # noqa: F401


registered_commands = [
    (Commands.create_interactions_result, messages.CreateInteractions(), simple_callbacks.simple_callback_arg_unpack),
    (Commands.get_interactions_response, messages.GetInteractions(), simple_callbacks.simple_callback_arg),
]


registered_messages = [
    (Messages.create_interactions, messages.CreateInteractions()),
    (Messages.get_interactions, messages.GetInteractions()),
    (Messages.delete_interactions, messages.DeleteInteractions()),
    (Messages.interactions_calc_done, messages.InteractionsCalcDone()),
]

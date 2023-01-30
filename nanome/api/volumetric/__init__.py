from .models import UnitCell, VolumeData, VolumeLayer, VolumeProperties  # noqa: F401
from . import serializers  # noqa: F401

# folders
from . import io, messages  # noqa: F401


from nanome._internal.enums import Commands, Messages
from nanome.util import simple_callbacks

registered_commands = [
    (Commands.add_volume_done, messages.AddVolumeDone(), simple_callbacks.simple_callback_no_arg),
]

registered_messages = [
    (Messages.add_volume, messages.AddVolume())
]

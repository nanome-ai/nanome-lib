from . import *  # noqa: F401
from .shape import Shape  # noqa: F401
from .sphere import Sphere  # noqa: F401
from .line import Line  # noqa: F401
from .label import Label  # noqa: F401
from .anchor import Anchor  # noqa: F401
from .mesh import Mesh  # noqa: F401
from . import serializers, messages  # noqa: F401

from nanome._internal.enums import Commands, Messages
from nanome.util import simple_callbacks


registered_commands = [
    (Commands.set_shape_result, messages.SetShape(), simple_callbacks.simple_callback_arg_unpack),
    (Commands.delete_shape_result, messages.DeleteShape(), simple_callbacks.simple_callback_arg),
]


registered_messages = [
    (Messages.set_shape, messages.SetShape()),
    (Messages.delete_shape, messages.DeleteShape()),
]

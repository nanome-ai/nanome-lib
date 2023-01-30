from .models import Room  # noqa: F401
from . import messages  # noqa: F401

from nanome._internal.enums import Messages


registered_commands = []
registered_messages = [
    (Messages.set_skybox, messages.SetSkybox()),
]

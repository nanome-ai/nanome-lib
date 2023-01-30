from . import *
from .integration_request import IntegrationRequest  # noqa: F401
from .integration import Integration  # noqa: F401
from . import messages, callbacks  # noqa: F401

from nanome._internal.enums import Commands, Messages


registered_commands = [
    (Commands.integration, messages.IntegrationSerializer(), callbacks.integration),
]


registered_messages = [
    (Messages.integration, messages.IntegrationSerializer()),
]

import asyncio
import json
import graypy
import logging
import os
import random
import string

from nanome.util.config import str2bool
from nanome._internal.network.packet import Packet

# from tblib import pickling_support
# pickling_support.install()

logger = logging.getLogger(__name__)


class RemoteLoggingFilter(logging.Filter):

    def filter(self, record):
        """Filter out log messages when remote logging is set to False."""
        return str2bool(os.environ.get('PLUGIN_REMOTE_LOGGING', 'False'))


class SessionLoggingHandler(graypy.handler.BaseGELFHandler):
    """Forward Log messages from session to NTS stream."""

    def __init__(self, nts_writer, plugin_id, plugin_name, session_id=None, plugin_instance=None):
        super(SessionLoggingHandler, self).__init__(level_names=True)
        self.writer = nts_writer
        # Server Fields
        self.plugin_id = plugin_id
        self.plugin_name = plugin_name
        self.session_id = session_id
        self.plugin_instance = plugin_instance

        if session_id:
            # Appending random string to process name makes tracking unique sessions easier
            random_str = ''.join(random.choices(string.ascii_lowercase + string.digits, k=6))
            process_name = "Session-{}-{}".format(session_id, random_str)
        else:
            process_name = "MainProcess"
        self.process_name = process_name

        # Session Fields, set by set_presenter_info
        self.org_name = None
        self.org_id = None
        self.account_id = None
        self.account_name = None

    def handle(self, record):
        # Add extra fields to the record.
        record.__dict__.update({
            'plugin_name': self.plugin_name,
            'plugin_class': self.plugin_instance.__class__.__name__,
            'plugin_id': self.plugin_id,
            'source_type': 'Plugin',
            'org_name': self.org_name,
            'org_id': self.org_id,
            'user_id': self.account_id,
            'username': self.account_name,
            # 'nts_host': self._plugin.host,
        })
        record.processName = self.process_name
        return super(SessionLoggingHandler, self).handle(record)

    def emit(self, record):
        gelf_dict = self._make_gelf_dict(record)
        packet = Packet()
        packet.set(0, Packet.packet_type_live_logs, 0)
        packet.write_string(json.dumps(gelf_dict))
        self.writer.write(packet.pack())

    async def set_presenter_info(self):
        """Get presenter info from plugin instance and store on handler."""
        client = self.plugin_instance.client
        presenter_info = await client.request_presenter_info()
        # If client.deserialize_payloads is disabled, we need to manually
        # deserialize the payload.
        if not client.deserialize_payloads and isinstance(presenter_info, bytearray):
            presenter_info = client._deserialize_payload(presenter_info)
        self.org_id = presenter_info.org_id
        self.org_name = presenter_info.org_name
        self.account_id = presenter_info.account_id
        self.account_name = presenter_info.account_name
        logger.debug("Presenter info set.")
        return presenter_info


def configure_main_process_logging(nts_writer, plugin_id, plugin_name):
    """Configure logging handler to send logs to NTS stream."""
    default_logging_config_ini = os.path.join(os.path.dirname(__file__), 'logging_config.ini')
    logging.config.fileConfig(default_logging_config_ini, disable_existing_loggers=False)
    logger = logging.getLogger()

    session_handler = SessionLoggingHandler(nts_writer, plugin_id, plugin_name)
    session_handler.addFilter(RemoteLoggingFilter())

    verbose = str2bool(os.environ.get("PLUGIN_VERBOSE", False))
    level = logging.DEBUG if verbose else logging.INFO
    logger.setLevel(level)
    logger.addHandler(session_handler)
    session_logger = logging.getLogger("sessions")
    session_logger.setLevel(level)


async def configure_session_logging(nts_writer, plugin_id, plugin_name, session_id, plugin_instance):
    """Configure logging handler to send logs to main process."""
    logger = logging.getLogger()
    verbose = str2bool(os.environ.get("PLUGIN_VERBOSE"))
    level = logging.DEBUG if verbose else logging.INFO
    logger.setLevel(level)
    session_handler = SessionLoggingHandler(nts_writer, plugin_id, plugin_name, session_id, plugin_instance)
    logger.addHandler(session_handler)
    asyncio.create_task(session_handler.set_presenter_info())

from nanome._internal.enums import Commands, Messages, IntegrationCommands, Permissions
from nanome.util.enums import Integrations
import logging

logger = logging.getLogger(__name__)


class Hashes():
    """Hashes used to identify commands and messages by NTS."""

    CommandHashes = [None] * len(Commands)
    MessageHashes = [None] * len(Messages)
    IntegrationHashes = [None] * len(IntegrationCommands)
    IntegrationRequestHashes = [None] * len(Integrations)
    PermissionRequestHashes = [None] * len(Permissions)
    HashToIntegrationName = dict()

    @staticmethod
    def hash_command(str):
        result = 0
        hit = 0
        a_char_value = ord('a')
        z_char_value = ord('z')
        for i in range(6):
            idx = i * 3 % len(str)
            char_value = ord(str[idx].lower()) - a_char_value
            result <<= 5
            if char_value < 0 or char_value > z_char_value - a_char_value:
                continue
            result |= char_value + 1
            hit += 1
            if hit >= 6:
                break
        return result

    @classmethod
    def init_hashes(cls):
        hashes = dict()
        i = -1
        for command in Commands:
            i += 1
            hash = cls.hash_command(command.name)
            if hash in hashes:
                logger.error("Command hash collision detected: {} and {}".format(command.name, hashes[hash]))
                continue
            hashes[hash] = command.name
            cls.CommandHashes[i] = hash

        hashes.clear()
        i = -1

        for command in Messages:
            i += 1
            hash = cls.hash_command(command.name)
            if hash in hashes:
                logger.error("Message hash collision detected: {} and {}".format(command.name, hashes[hash]))
                continue
            hashes[hash] = command.name
            cls.MessageHashes[i] = hash

        hashes.clear()
        i = -1

        for command in IntegrationCommands:
            i += 1
            hash = cls.hash_command(command.name)
            if hash in hashes:
                logger.error("Integration hash collision detected: {} and {}".format(command.name, hashes[hash]))
                continue
            hashes[hash] = command.name
            cls.IntegrationHashes[i] = hash
            cls.HashToIntegrationName[hash] = command.name

        hashes.clear()
        i = -1

        for command in Integrations:
            i += 1
            hash = cls.hash_command(command.name)
            if hash in hashes:
                logger.error("Integration request hash collision detected: {} and {}".format(command.name, hashes[hash]))
                continue
            hashes[hash] = command.name
            cls.IntegrationRequestHashes[i] = hash

        hashes.clear()
        i = -1
        for command in Permissions:
            i += 1
            hash = cls.hash_command(command.name)
            if hash in hashes:
                logger.error("Permission request hash collision detected: {} and {}".format(command.name, hashes[hash]))
                continue
            hashes[hash] = command.name
            cls.PermissionRequestHashes[i] = hash

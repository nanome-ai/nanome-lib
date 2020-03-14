from nanome.util import Logs
from abc import ABCMeta, abstractmethod

__metaclass__ = type
class _TypeSerializer(object):
    __metaclass__ = ABCMeta
    __version_table = dict()

    def __new__(cls, *args):
        result = super(_TypeSerializer, cls).__new__(cls)
        cls.register_string_raw(result.name(), result.version())
        result.__init__(*args)
        return result

    @classmethod
    def register_string_raw(cls, string, version):
        cls.__version_table[string] = version


    @classmethod
    def get_version_table(cls):
        return cls.__version_table

    @classmethod
    def get_best_version_table(cls, nanome_table):
        result = dict()
        version_table = cls.__version_table
        for key in nanome_table:
            nanome_version = nanome_table[key]
            try:
                version = version_table[key]
                result[key] = min(version, nanome_version)
            except:
                Logs.warning("Plugin Library might be outdated: received a serializer version for an unknown serializer:", key, "Version:", nanome_version)
        return result

    @abstractmethod
    def name(self):
        # type() -> str
        pass

    @abstractmethod
    def version(self):
        # type() -> int
        pass
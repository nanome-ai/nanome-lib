from nanome._internal._util._serializers import _ArraySerializer
from nanome._internal._util._serializers import _TypeSerializer
from nanome.util.file import LoadInfoDone
from nanome.util.enums import LoadFileErrorCode


class _LoadFileDoneInfo(_TypeSerializer):
    def __init__(self):
        pass

    def version(self):
        return 0

    def name(self):
        return "LoadFileDoneInfo"

    def serialize(self, version, value, context):
        raise NotImplementedError

    def deserialize(self, version, context):
        result = LoadInfoDone()
        result.success = LoadFileErrorCode(context.read_byte())
        return result


class _LoadFileDone(_TypeSerializer):
    def __init__(self):
        self.array = _ArraySerializer()
        self.array.set_type(_LoadFileDoneInfo())

    def version(self):
        return 0

    def name(self):
        return "LoadFileDone"

    def serialize(self, version, value, context):
        raise NotImplementedError

    def deserialize(self, version, context):
        return context.read_using_serializer(self.array)

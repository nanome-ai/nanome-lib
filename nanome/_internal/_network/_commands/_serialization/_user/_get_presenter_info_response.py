from nanome._internal._util._serializers import _TypeSerializer, _StringSerializer
from nanome.api.user import PresenterInfo


class _GetPresenterInfoResponse(_TypeSerializer):
    def __init__(self):
        self.string = _StringSerializer()

    def version(self):
        return 0

    def name(self):
        return "GetPresenterInfoResponse"

    def serialize(self, version, value, context):
        pass

    def deserialize(self, version, context):
        result = PresenterInfo()
        result.account_id = context.read_using_serializer(self.string)
        result.account_name = context.read_using_serializer(self.string)
        result.account_email = context.read_using_serializer(self.string)

        return result

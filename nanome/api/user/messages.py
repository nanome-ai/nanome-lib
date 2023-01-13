from nanome._internal import serializer_fields
from . import PresenterInfo


class GetPresenterInfo(serializer_fields.TypeSerializer):
    def version(self):
        return 0

    def name(self):
        return "GetPresenterInfo"

    def serialize(self, version, value, data):
        pass

    def deserialize(self, version, data):
        return None


class GetPresenterInfoResponse(serializer_fields.TypeSerializer):

    def __init__(self):
        self.string = serializer_fields.StringField()

    def version(self):
        return 1

    def name(self):
        return "GetPresenterInfoResponse"

    def serialize(self, version, value, context):
        pass

    def deserialize(self, version, context):

        result = PresenterInfo()
        result.account_id = context.read_using_serializer(self.string)
        result.account_name = context.read_using_serializer(self.string)
        result.account_email = context.read_using_serializer(self.string)
        result.has_org = context.read_bool()
        if result.has_org:
            result.org_id = context.read_int()
            result.org_name = context.read_using_serializer(self.string)

        return result


class PresenterChange(serializer_fields.TypeSerializer):
    def version(self):
        return 0

    def name(self):
        return "PresenterChange"

    def serialize(self, version, value, data):
        pass

    def deserialize(self, version, data):
        return None

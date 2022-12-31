from nanome._internal._util._serializers import _TypeSerializer


class _ImportFile(_TypeSerializer):

    def version(self):
        return 0

    def name(self):
        return "ImportFile"

    def serialize(self, version, value, context):
        pass

    def deserialize(self, version, context):
        return

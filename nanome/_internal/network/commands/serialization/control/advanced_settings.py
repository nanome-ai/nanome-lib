from nanome._internal.util.serializers import TypeSerializer


class _AdvancedSettings(TypeSerializer):
    def __init__(self):
        pass

    def version(self):
        return 0

    def name(self):
        return "AdvancedSettings"

    def serialize(self, version, value, data):
        pass

    def deserialize(self, version, data):
        return None

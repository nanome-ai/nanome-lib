import logging
from nanome._internal import serializer_fields
from . import serializers

logger = logging.getLogger(__name__)


class CreateInteractions(serializer_fields.TypeSerializer):
    def __init__(self):
        self._interaction = serializers.InteractionSerializer()
        self._interaction_array = serializer_fields.ArrayField()
        self._interaction_array.set_type(self._interaction)

    def version(self):
        return 1

    def name(self):
        return "CreateInteractions"

    def serialize(self, version, value, context):
        context.write_using_serializer(self._interaction_array, value)

    def deserialize(self, version, context):
        return context.read_long_array()


class DeleteInteractions(serializer_fields.TypeSerializer):
    def version(self):
        return 1

    def name(self):
        return "DeleteInteractions"

    def serialize(self, version, value, context):
        context.write_long_array(value)

    def deserialize(self, version, context):
        raise NotImplementedError()


class GetInteractions(serializer_fields.TypeSerializer):
    def __init__(self):
        self._interaction = serializers.InteractionSerializer()
        self._interaction_array = serializer_fields.ArrayField()
        self._interaction_array.set_type(self._interaction)

    def version(self):
        return 1

    def name(self):
        return "GetInteractions"

    def serialize(self, version, value, context):
        context.write_long_array(value[0])
        context.write_long_array(value[1])
        context.write_long_array(value[2])
        context.write_long_array(value[3])
        context.write_long_array(value[4])
        context.write_byte(int(value[5]))

    def deserialize(self, version, context):
        return context.read_using_serializer(self._interaction_array)


class InteractionsCalcDone(serializer_fields.TypeSerializer):
    def version(self):
        return 0

    def name(self):
        return "InteractionsCalcDone"

    def serialize(self, version, value, context):
        pass

    def deserialize(self, version, context):
        raise NotImplementedError()

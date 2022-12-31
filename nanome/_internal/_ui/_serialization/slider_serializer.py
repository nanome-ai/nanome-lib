from nanome.util import IntEnum
from .. import _Slider
from . import _UIBaseSerializer

from nanome._internal._util._serializers import _TypeSerializer


class _SliderSerializer(_TypeSerializer):
    def __init__(self):
        pass

    def version(self):
        return 1

    def name(self):
        return "Slider"

    def serialize(self, version, value, context):
        if (version == 0):
            safe_id = (context._plugin_id << 24) & 0x7FFFFFFF
            safe_id |= value._content_id
        else:
            safe_id = value._content_id
        context.write_int(safe_id)
        context.write_float(value._current_value)
        context.write_float(value._min_value)
        context.write_float(value._max_value)
        pass

    def deserialize(self, version, context):
        value = _Slider._create()
        value._content_id = context.read_int()
        if (version == 0):
            id_mask = 0x00FFFFFF
            value._content_id &= id_mask
        value._current_value = context.read_float()
        value._min_value = context.read_float()
        value._max_value = context.read_float()
        return value


_UIBaseSerializer.register_type("Slider", _UIBaseSerializer.ContentType.eslider, _SliderSerializer())


from nanome._internal.util.serializers import TypeSerializer


class _ButtonCallback(TypeSerializer):
    def __init__(self):
        pass

    def version(self):
        return 2

    def name(self):
        return "ButtonCallback"

    def serialize(self, version, value, context):
        id = value[0]
        state = value[1]
        if (version == 0):
            plugin_mask = (context._plugin_id << 24) & 0x7FFFFFFF
            id |= plugin_mask
        context.write_int(id)
        if version >= 2:
            context.write_bool(state)

    def deserialize(self, version, context):
        content_id = context.read_int()
        if (version == 0):
            id_mask = 0x00FFFFFF
            content_id &= id_mask
        state = False
        if version >= 2:
            state = context.read_bool()
        return (content_id, state)


from nanome._internal.util.serializers import TypeSerializer


class _DropdownCallback(TypeSerializer):
    def __init__(self):
        pass

    def version(self):
        return 0

    def name(self):
        return "DropdownCallback"

    def serialize(self, version, value, context):
        # value is a tuple containing the image ID and the item index.
        context.write_int(value[0])
        context.write_int(value[1])

    def deserialize(self, version, context):
        id = context.read_int()
        item_index = context.read_int()
        return id, item_index
from nanome._internal.util.serializers import TypeSerializer


class _GetMenuTransform(TypeSerializer):
    def __init__(self):
        pass

    def version(self):
        return 0

    def name(self):
        return "GetMenuTransform"

    def serialize(self, version, value, context):
        context.write_byte(value)

    def deserialize(self, version, context):
        return None
from nanome._internal.util.serializers import TypeSerializer, _UnityPositionSerializer, _UnityRotationSerializer, _Vector3Serializer


class _GetMenuTransformResponse(TypeSerializer):
    def __init__(self):
        self.pos = _UnityPositionSerializer()
        self.rot = _UnityRotationSerializer()
        self.vec3 = _Vector3Serializer()

    def version(self):
        return 0

    def name(self):
        return "GetMenuTransformResponse"

    def serialize(self, version, value, context):
        pass

    def deserialize(self, version, context):
        menu_position = context.read_using_serializer(self.pos)
        menu_rotation = context.read_using_serializer(self.rot)
        menu_scale = context.read_using_serializer(self.vec3)

        result = (menu_position, menu_rotation, menu_scale)
        return result
from nanome._internal.util.serializers import TypeSerializer


class _ImageCallback(TypeSerializer):
    def __init__(self):
        pass

    def version(self):
        return 1

    def name(self):
        return "ImageCallback"

    def serialize(self, version, value, context):
        # value is a tuple containing the image ID, the x coordinate and the y coordinate.
        if (version == 0):
            plugin_mask = (context._plugin_id << 24) & 0x7FFFFFFF
            value = (value[0] | plugin_mask, value[1], value[2])
        context.write_int(value[0])
        context.write_float(value[1])
        context.write_float(value[2])

    def deserialize(self, version, context):
        id = context.read_int()
        if (version == 0):
            id_mask = 0x00FFFFFF
            id &= id_mask
        x = context.read_float()
        y = context.read_float()
        return id, x, y
from nanome._internal.util.serializers import TypeSerializer


class _MenuCallback(TypeSerializer):
    def __init__(self):
        pass

    def version(self):
        return 1

    def name(self):
        return "MenuCallback"

    def serialize(self, version, value, context):
        if version >= 1:
            context.write_byte(value[0])
        context.write_bool(value[1])

    def deserialize(self, version, context):
        if version >= 1:
            index = context.read_byte()
        else:
            index = 0
        value = context.read_bool()
        return (index, value)
from nanome._internal.util.serializers import _Vector3Serializer, _UnityPositionSerializer, _UnityRotationSerializer, TypeSerializer


class _SetMenuTransform(TypeSerializer):
    def __init__(self):
        self.pos = _UnityPositionSerializer()
        self.rot = _UnityRotationSerializer()
        self.vec3 = _Vector3Serializer()

    def version(self):
        return 0

    def name(self):
        return "SetMenuTransform"

    def serialize(self, version, value, data):
        data.write_byte(value[0])
        data.write_using_serializer(self.pos, value[1])
        data.write_using_serializer(self.rot, value[2])
        data.write_using_serializer(self.vec3, value[3])

    def deserialize(self, version, data):
        return None
from nanome._internal.util.serializers import TypeSerializer


class _SliderCallback(TypeSerializer):
    def version(self):
        return 1

    def name(self):
        return "SliderCallback"

    def serialize(self, version, value, context):
        if (version == 0):
            plugin_mask = (context._plugin_id << 24) & 0x7FFFFFFF
            value[0] |= plugin_mask
        context.write_int(value[0])
        context.write_float(value[1])

    def deserialize(self, version, context):
        content_id = context.read_int()
        if (version == 0):
            id_mask = 0x00FFFFFF
            content_id &= id_mask
        result = (content_id, context.read_float())
        return result
from nanome._internal.util.serializers import TypeSerializer, _TupleSerializer, _IntSerializer, _StringSerializer


class _TextInputCallback(TypeSerializer):
    def __init__(self):
        self.__tuple = _TupleSerializer(_IntSerializer(), _StringSerializer())

    def version(self):
        return 1

    def name(self):
        return "TextInputCallback"

    def serialize(self, version, value, context):
        if (version == 0):
            plugin_mask = (context._plugin_id << 24) & 0x7FFFFFFF
            value[0] |= plugin_mask
        context.write_using_serializer(self.__tuple, value)

    def deserialize(self, version, context):
        tup = context.read_using_serializer(self.__tuple)
        if (version == 0):
            id_mask = 0x00FFFFFF
            tup = (tup[0] & id_mask, tup[1])
        return tup
from nanome._internal.util.serializers import TypeSerializer
from nanome.util import IntEnum


class _UIHook(TypeSerializer):
    class Type(IntEnum):
        button_hover = 0
        image_pressed = 1
        image_held = 2
        image_released = 3

    def __init__(self):
        pass

    def version(self):
        return 0

    def name(self):
        return "UIHook"

    def serialize(self, version, value, context):
        context.write_byte(value[0])
        context.write_int(value[1])

    def deserialize(self, version, context):
        raise NotImplementedError
from nanome._internal.ui._serialization import _UIBaseSerializer
from nanome._internal.util.serializers import _ArraySerializer
from nanome._internal.util.serializers import TypeSerializer


class _UpdateContent(TypeSerializer):
    def __init__(self):
        self._array = _ArraySerializer()
        self._content = _UIBaseSerializer()
        self._array.set_type(self._content)

    def version(self):
        return 1

    def name(self):
        return "SendUIContent"

    def serialize(self, version, value, context):
        if version == 0:
            context.write_using_serializer(self._content, value[0])
        else:
            context.write_using_serializer(self._array, value)

    def deserialize(self, version, context):
        return None
from nanome._internal.util.serializers import _ArraySerializer
from nanome._internal.ui._serialization import _LayoutNodeSerializer, _UIBaseSerializer, _MenuSerializer

from nanome._internal.util.serializers import TypeSerializer


class _UpdateMenu(TypeSerializer):
    def __init__(self):
        self.menu = _MenuSerializer()
        self.array = _ArraySerializer()
        self.layout = _LayoutNodeSerializer()
        self.content = _UIBaseSerializer()

    def version(self):
        return 2

    def name(self):
        return "UpdateMenu"

    def serialize(self, version, value, context):
        (menu, shallow) = value
        if version >= 1:
            context.write_byte(menu.index)
        if version >= 2:
            context.write_bool(shallow)

        context.write_using_serializer(self.menu, menu)
        nodes = []
        content = []
        if not shallow:
            nodes = menu._get_all_nodes()
            content = menu._get_all_content()
        self.array.set_type(self.layout)
        context.write_using_serializer(self.array, nodes)
        self.array.set_type(self.content)
        context.write_using_serializer(self.array, content)

    def deserialize(self, version, context):
        return None
from nanome._internal.ui._serialization import _LayoutNodeSerializerDeep
from nanome._internal.util.serializers import _ArraySerializer
from nanome._internal.util.serializers import TypeSerializer


class _UpdateNode(TypeSerializer):
    def __init__(self):
        self._array = _ArraySerializer()
        self._node_serializer = _LayoutNodeSerializerDeep()
        self._array.set_type(self._node_serializer)

    def version(self):
        return 1

    def name(self):
        return "SendLayoutNode"

    def serialize(self, version, value, context):
        if version == 0:
            context.write_using_serializer(self._node_serializer, value[0])
        else:
            context.write_using_serializer(self._array, value)

    def deserialize(self, version, context):
        return None

from nanome._internal.serializer_fields import TypeSerializer, ArrayField, ColorField, StringField


class UnitCellSerializer(TypeSerializer):

    def version(self):
        return 0

    def name(self):
        return "UnitCell"

    def serialize(self, version, value, context):
        context.write_float(value._A)
        context.write_float(value._B)
        context.write_float(value._C)
        context.write_float(value._Alpha)
        context.write_float(value._Beta)
        context.write_float(value._Gamma)
        context.write_float(value._Origin.x)
        context.write_float(value._Origin.y)
        context.write_float(value._Origin.z)

    def deserialize(self, version, context):
        raise NotImplementedError


class VolumeDataSerializer(TypeSerializer):
    __string = StringField()
    __cell = UnitCellSerializer()

    def version(self):
        return 0

    def name(self):
        return "VolumeData"

    def serialize(self, version, value, context):
        context.write_int(value._width)
        context.write_int(value._height)
        context.write_int(value._depth)

        context.write_float(value._mean)
        context.write_float(value._rmsd)
        context.write_int(value._type)
        context.write_using_serializer(
            VolumeDataSerializer.__string, value._name)
        context.write_using_serializer(
            VolumeDataSerializer.__cell, value._cell)

        context.write_float_array(value._data)

    def deserialize(self, version, context):
        raise NotImplementedError


class VolumeLayerSerializer(TypeSerializer):
    __color = ColorField()

    def version(self):
        return 0

    def name(self):
        return "VolumeLayer"

    def serialize(self, version, value, context):
        context.write_using_serializer(
            VolumeLayerSerializer.__color, value._color)
        context.write_float(value._rmsd)

    def deserialize(self, version, context):
        raise NotImplementedError


class VolumePropertiesSerializer(TypeSerializer):
    def __init__(self):
        self.__array = ArrayField()
        self.__array.set_type(VolumeLayerSerializer())

    def version(self):
        return 0

    def name(self):
        return "VolumeProperties"

    def serialize(self, version, value, context):
        context.write_bool(value._visible)
        context.write_bool(value._boxed)
        context.write_bool(value._use_map_mover)
        context.write_int(int(value._style))
        context.write_using_serializer(self.__array, value._layers)

    def deserialize(self, version, context):
        raise NotImplementedError

from nanome._internal.serializer_fields import TypeSerializer, ColorField
import logging
from . import Interaction

logger = logging.getLogger(__name__)


class InteractionSerializer(TypeSerializer):
    def __init__(self):
        self._color = ColorField()

    def version(self):
        return 0

    def name(self):
        return "Interaction"

    def serialize(self, version, value, context):
        context.write_long(value._index if value._index is not None else -1)
        context.write_byte(int(value._kind))
        context.write_long(value._atom1_idx)
        context.write_long(value._atom2_idx)
        if value._atom1_conformation is not None:
            context.write_bool(True)
            context.write_int(value._atom1_conformation)
        else:
            context.write_bool(False)
        if value._atom2_conformation is not None:
            context.write_bool(True)
            context.write_int(value._atom2_conformation)
        else:
            context.write_bool(False)
        context.write_using_serializer(self._color, value._color)

    def deserialize(self, version, context):
        from nanome.util.enums import InteractionKind
        idx = context.read_long()
        kind = InteractionKind.safe_cast(context.read_byte())
        atom1 = context.read_long()
        atom2 = context.read_long()
        if context.read_bool() is True:
            atom1_conf = context.read_int()
        else:
            atom1_conf = None
        if context.read_bool() is True:
            atom2_conf = context.read_int()
        else:
            atom2_conf = None
        color = context.read_using_serializer(self._color)
        
        result = Interaction(kind, color, atom1, atom2, atom1_conf, atom2_conf)
        result._index = idx

        return result
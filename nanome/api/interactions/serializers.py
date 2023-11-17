from nanome._internal.serializer_fields import TypeSerializer
import logging
from . import Interaction

logger = logging.getLogger(__name__)


class InteractionSerializer(TypeSerializer):
    def version(self):
        return 1

    def name(self):
        return "Interaction"

    def serialize(self, version, value, context):
        context.write_long(value.index)
        context.write_byte(int(value.kind))
        context.write_long_array(value.atom1_idx_arr)
        context.write_long_array(value.atom2_idx_arr)
        if value.atom1_conformation is not None:
            context.write_bool(True)
            context.write_int(value.atom1_conformation)
        else:
            context.write_bool(False)
        if value.atom2_conformation is not None:
            context.write_bool(True)
            context.write_int(value.atom2_conformation)
        else:
            context.write_bool(False)
        context.write_bool(value.visible)

    def deserialize(self, version, context):
        from nanome.util.enums import InteractionKind
        idx = context.read_long()
        kind = InteractionKind.safe_cast(context.read_byte())
        atom1_arr = context.read_long_array()
        atom2_arr = context.read_long_array()
        if context.read_bool() is True:
            atom1_conf = context.read_int()
        else:
            atom1_conf = None
        if context.read_bool() is True:
            atom2_conf = context.read_int()
        else:
            atom2_conf = None
        visible = context.read_bool()

        result = Interaction(kind, atom1_arr, atom2_arr, atom1_conf, atom2_conf, visible)
        result.index = idx

        return result

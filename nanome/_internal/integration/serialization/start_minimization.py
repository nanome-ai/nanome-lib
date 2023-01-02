from nanome._internal.util.serializers import TypeSerializer


class _StartMinimization(TypeSerializer):
    def version(self):
        return 0

    def name(self):
        return "StartMinimization"

    def serialize(self, version, value, context):
        context.write_bool(value)

    def deserialize(self, version, context):
        forcefield = context.read_byte()
        steps = context.read_int()
        steepest = context.read_bool()
        cutoff = context.read_float()
        return (forcefield, steps, steepest, cutoff)

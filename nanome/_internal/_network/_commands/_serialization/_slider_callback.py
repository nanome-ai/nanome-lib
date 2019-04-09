from nanome._internal._util._serializers import _TypeSerializer

class _SliderCallback(_TypeSerializer):
    def version(self):
        return 0

    def name(self):
        return "SliderCallback"
        
    def serialize(self, version, value, context):
        context.write_int(value[0])
        context.write_float(value[1])

    def deserialize(self, version, context):
        result = (context.read_int(), context.read_float())
        return result

from nanome._internal._util._serializers import _TypeSerializer

class _ImageCallback(_TypeSerializer):
    def __init__(self):
        pass

    def version(self):
        return 0

    def name(self):
        return "ImageCallback"
        
    def serialize(self, version, value, context):
        #value is a tuple containing the image ID, the x coordinate and the y coordinate.
        context.write_int(value[0])
        context.write_float(value[1])
        context.write_float(value[2])

    def deserialize(self, version, context):
        id = context.read_int()
        x = context.read_float()
        y = context.read_float()
        return id, x, y

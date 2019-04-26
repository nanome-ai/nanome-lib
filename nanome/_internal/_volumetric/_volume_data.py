class _VolumeData(object):
    def __init__(self, 
                 size_x, size_y, size_z, 
                 delta_x, delta_y, delta_z):
        #byte array for speed.
        #if we later speed up array serializer
        #or make this an API, we should
        #convert to float []
        self._data = [] 

        self._size_x = size_x
        self._size_y = size_y
        self._size_z = size_z
        
        self._delta_x = delta_x
        self._delta_y = delta_y
        self._delta_z = delta_z

        self._origin_x = 0.0
        self._origin_y = 0.0
        self._origin_z = 0.0
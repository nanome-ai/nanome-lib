class _Addon(object):
    def __init__(self, base_object=None):
        self.base_object = base_object
        if base_object != None:
            self.base_class = base_object.__class__

    def _setup_addon(self, base_class):
        self.base_class = base_class
class Content(object):
    def __init__(self):
        self.name = ""
        self.models = []
    
    class Atom(object):
        def __init__(self):
            self.serial = 0
            self.x = 0
            self.y = 0
            self.z = 0
            self.symbol = "c"
            self.mass = 0
            self.charge = 0

    class Bond(object):
        def __init__(self):
            self.serial = 0
            self.serial_atom1 = 0
            self.serial_atom2 = 0
            self.bond_order = 0

    class Model(object):
        def __init__(self):
            self.name = ""
            self.author = ""
            self.comment = ""
            self.version = "V2000"
            self.atoms = []
            self.bonds = []
            self.properties = [] #strings
            self._associated = {} #<string, strings>
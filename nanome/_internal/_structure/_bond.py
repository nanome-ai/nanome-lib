from . import _Base
import nanome

class _Bond(_Base):
    Kind = nanome.util.enums.Kind

    @classmethod
    def _create(cls):
        return cls()

    def __init__(self):
        super(_Bond, self).__init__()
        self.__atom1 = None
        self.__atom2 = None
        self._parent = None

        self._in_conformer = [True]
        self._kinds = [_Bond.Kind.CovalentSingle]

    @property
    def _atom1(self):
        return self.__atom1

    @_atom1.setter
    def _atom1(self, value):
        if self.__atom1 is not None:
            try:
                self.__atom1._bonds.remove(self)
            except ValueError:
                pass
        if value is not None:
            value._bonds.append(self)
        self.__atom1 = value

    @property
    def _atom2(self):
        return self.__atom2

    @_atom2.setter
    def _atom2(self, value):
        if self.__atom2 is not None:
            try:
                self.__atom2._bonds.remove(self)
            except ValueError:
                pass
        if value is not None:
            value._bonds.append(self)
        self.__atom2 = value

    #region connections
    @property
    def _residue(self):
        return self._parent

    @property
    def _chain(self):
        parent = self._parent
        if parent:
            return parent._chain
        else:
            return None

    @property
    def _molecule(self):
        parent = self._parent
        if parent:
            return parent._molecule
        else:
            return None

    @property
    def _complex(self):
        parent = self._parent
        if parent:
            return parent._complex
        else:
            return None
    #endregion

    #region conformer stuff
    @property
    def _current_conformer(self):
        if self._molecule != None:
            return self._molecule._current_conformer
        else:
            return 0

    @property
    def _conformer_count(self):
        if self._molecule != None:
            return self._molecule._conformer_count
        else:
            return 1

    def _resize_conformer(self, new_size):
        curr_size = len(self._kinds)
        if new_size > curr_size:
            extension = new_size - curr_size
            self._kinds.extend([self._kinds[-1]]*(extension))
            self._in_conformer.extend([self._in_conformer[-1]]*(extension))
        else:
            self._kinds = self._kinds[:new_size]
            self._in_conformer = self._in_conformer[:new_size]

    def _move_conformer(self, src, dest):
        temp = self._in_conformer[src]
        self._in_conformer.insert(dest, temp)
        temp = self._kinds[src]
        self._kinds.insert(dest, temp)
        src = src + 1 if src > dest else src
        del self._in_conformer[src]
        del self._kinds[src]

    def _delete_conformer(self, index):
        del self._kinds[index]
        del self._in_conformer[index]

    def _copy_conformer(self, src, index= None):
        if index is None:
            index = src
        value = self._in_conformer[src]
        self._in_conformer.insert(index, value)
        value = self._kinds[src]
        self._kinds.insert(index, value)

    @property
    def _kind(self):
        return self._kinds[self._current_conformer]

    @_kind.setter
    def _kind(self, value):
        self._kinds[self._current_conformer] = value

    @property
    def _exists(self):
        return self._in_conformer[self._current_conformer]
    
    @_exists.setter
    def _exists(self, value):
        self._in_conformer[self._current_conformer] = value
    #endregion

    #copies the structure. If conformer_number is not None it will only copy that conformer's data.
    def _shallow_copy(self, conformer_number = None):
        bond = _Bond._create()
        if conformer_number == None:
            bond._in_conformer = list(self._in_conformer)
            bond._kinds = list(self._kinds)
        else:
            bond._kind = self._kinds[conformer_number]
            # bond._exists = self._in_conformer[conformer_number]
        return bond

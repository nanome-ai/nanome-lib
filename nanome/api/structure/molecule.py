import nanome
from nanome._internal._structure._molecule import _Molecule
from nanome._internal._network import _ProcessNetwork
from nanome._internal import _PluginInstance
from nanome._internal._network._commands._callbacks import _Messages

from nanome.util import Logs
from . import Base


class Molecule(_Molecule, Base):
    """
    | Represents a molecule. Contains chains.
    """

    def __init__(self):
        super(Molecule, self).__init__()
        self._molecular = Molecule.Molecular(self)

    def add_chain(self, chain):
        """
        | Add a chain to this molecule

        :param chain: Chain to add to the molecule
        :type chain: :class:`~nanome.structure.Chain`
        """
        chain.index = -1
        self._add_chain(chain)

    def remove_chain(self, chain):
        """
        | Remove a chain from this molecule

        :param chain: Chain to remove from the molecule
        :type chain: :class:`~nanome.structure.Chain`
        """
        chain.index = -1
        self._remove_chain(chain)

    # region Generators:
    @property
    def chains(self):
        """
        | The chains of this complex

        :type: :class:`generator` <:class:`~nanome.structure.Chain`>
        """
        for chain in self._chains:
            yield chain

    @property
    def residues(self):
        """
        | The residues of this complex

        :type: :class:`generator` <:class:`~nanome.structure.Residue`>
        """
        for chain in self.chains:
            for residue in chain.residues:
                yield residue

    @property
    def atoms(self):
        """
        | The atoms of this complex

        :type: :class:`generator` <:class:`~nanome.structure.Atom`>
        """
        for residue in self.residues:
            for atom in residue.atoms:
                yield atom

    @property
    def bonds(self):
        """
        | The bonds of this complex

        :type: :class:`generator` <:class:`~nanome.structure.Bond`>
        """
        for residue in self.residues:
            for bond in residue.bonds:
                yield bond
    # endregion

    # region connections
    @property
    def complex(self):
        """
        | Complex that the molecule belongs to
        """
        return self._complex
    # endregion

    # region all fields
    @property
    def name(self):
        """
        | Represents the name of the molecule

        :type: :class:`str`
        """
        return self._name

    @name.setter
    def name(self, value):
        if type(value) is not str:
            value = str(value)
        self._name = value

    @property
    def associated(self):
        """
        | Metadata associated with the molecule.
        | PDB REMARKs end up here.

        :type: :class:`dict`
        """
        return self._associated

    @associated.setter
    def associated(self, value):
        self._associated = value
    # endregion

    # region conformer stuff
    @property
    def names(self):
        return self._names

    @names.setter
    def names(self, value):
        if len(value) != self._conformer_count:
            raise ValueError("Length of associateds must match the conformer count of the molecule.")
        self._names = value

    @property
    def associateds(self):
        return self._associateds

    @associateds.setter
    def associateds(self, value):
        if len(value) != self._conformer_count:
            raise ValueError("Length of associateds must match the conformer count of the molecule.")
        self._associateds = value

    def set_conformer_count(self, count):
        self._conformer_count = count

    @property
    def conformer_count(self):
        return self._conformer_count

    def set_current_conformer(self, index):
        self._current_conformer = index

    @property
    def current_conformer(self):
        return self._current_conformer

    def create_conformer(self, index):
        self._create_conformer(index)

    def move_conformer(self, src, dest):
        self._move_conformer(src, dest)

    def delete_conformer(self, index):
        self._delete_conformer(index)

    def copy_conformer(self, src, index=None):
        self._copy_conformer(src, index)
    # endregion

    def get_substructures(self, callback=None):
        expects_response = callback is not None or nanome.PluginInstance._instance.is_async
        id = _ProcessNetwork._send(_Messages.substructure_request, (self.index, nanome.util.enums.SubstructureType.Unkown), expects_response)
        return nanome.PluginInstance._save_callback(id, callback)

    def get_ligands(self, callback=None):
        expects_response = callback is not None or nanome.PluginInstance._instance.is_async
        id = _ProcessNetwork._send(_Messages.substructure_request, (self.index, nanome.util.enums.SubstructureType.Ligand), expects_response)
        return nanome.PluginInstance._save_callback(id, callback)

    def get_proteins(self, callback=None):
        expects_response = callback is not None or nanome.PluginInstance._instance.is_async
        id = _ProcessNetwork._send(_Messages.substructure_request, (self.index, nanome.util.enums.SubstructureType.Protein), expects_response)
        return nanome.PluginInstance._save_callback(id, callback)

    def get_solvents(self, callback=None):
        expects_response = callback is not None or nanome.PluginInstance._instance.is_async
        id = _ProcessNetwork._send(_Messages.substructure_request, (self.index, nanome.util.enums.SubstructureType.Solvent), expects_response)
        return nanome.PluginInstance._save_callback(id, callback)

    # region deprecated
    @property
    @Logs.deprecated()
    def molecular(self):
        return self._molecular

    class Molecular(object):
        def __init__(self, parent):
            self.parent = parent

        @property
        def name(self):
            return self.parent.name

        @name.setter
        def name(self, value):
            self.parent.name = value
    # endregion


_Molecule._create = Molecule

import nanome
from nanome.util import Logs, enums
from nanome._internal.network import PluginNetwork
from nanome._internal.enums import Messages


class Interaction(object):
    """
    | Class representing a chemical interaction.

    :param kind: Enumerator representing the kind of interaction to create
    :type kind: :class:`~nanome.util.enums.InteractionType`
    :param atom1_idx: Array of integers representing the indices of atoms in group 1
    :type atom1_idx: List[int]
    :param atom2_idx: Array of integers representing the indices of atoms in group 2
    :type atom2_idx: List[int]
    :param atom1_conf: Optional conformation for all atoms in group 1
    :type atom1_conf: int
    :param atom2_conf: Optional conformation for all atoms in group 2
    :type atom2_conf: int
    """

    def __init__(self, kind=None, atom1_idx_arr=None, atom2_idx_arr=None, atom1_conf=None, atom2_conf=None):
        self.index = -1
        self.kind = kind
        self.atom1_idx_arr = atom1_idx_arr
        self.atom2_idx_arr = atom2_idx_arr
        self.atom1_conformation = atom1_conf
        self.atom2_conformation = atom2_conf

    def upload(self, done_callback=None):
        """
        | Upload the interaction to the Nanome App
        """
        return self._upload(done_callback)

    @classmethod
    def upload_multiple(cls, interactions, done_callback=None):
        """
        | Upload multiple interactions to the Nanome App
        """
        return cls._upload_multiple(interactions, done_callback)

    def destroy(self, done_callback=None):
        """
        | Remove the interaction from the Nanome App and destroy it.
        """
        return self._destroy(done_callback)

    @classmethod
    def destroy_multiple(cls, interactions):
        """
        | Remove multiple interactions from the Nanome App and destroy them.
        """
        return cls._destroy_multiple(interactions)
    
    @classmethod
    def get(cls, done_callback, complexes_idx=None, molecules_idx=None, chains_idx=None,
            residues_idx=None, atom_idx=None, type_filter=None):
        """
        | Get interactions from Nanome App
        | If no structure index is given, all interactions in workspace will be returned
        | If any combination of indices is given, all interactions for these sturctures will be returned

        :param done_callback: Callback called with the list of interactions received from Nanome
        :type done_callback: Callable[List[:class:`~nanome.api.interaction`]]
        :param ***_idx: Index or array of indices for a structure type
        :type ***_idx: int or List[int]
        :param type_filer: Filter to return only one type of interaction
        :type type_filer: :class:`~nanome.util.enums.InteractionType`
        """
        args = (
            complexes_idx if isinstance(complexes_idx, list) else [complexes_idx] if isinstance(complexes_idx, int) else [],
            molecules_idx if isinstance(molecules_idx, list) else [molecules_idx] if isinstance(molecules_idx, int) else [],
            chains_idx if isinstance(chains_idx, list) else [chains_idx] if isinstance(chains_idx, int) else [],
            residues_idx if isinstance(residues_idx, list) else [residues_idx] if isinstance(residues_idx, int) else [],
            atom_idx if isinstance(atom_idx, list) else [atom_idx] if isinstance(atom_idx, int) else [],
            type_filter if type_filter is not None else enums.InteractionKind.All
        )

        return cls._get_interactions(args, done_callback)

    def _upload(self, done_callback=None):
        if self.index != -1:
            Logs.error("An interaction can only be uploaded once")
            return

        def set_callback(indices):
            index = indices[0]
            self.index = index
            if done_callback is not None:
                done_callback()

        id = PluginNetwork._instance.send(Messages.create_interactions, [self], True)
        result = nanome.PluginInstance._save_callback(id, set_callback if done_callback else None)
        if done_callback is None and nanome.PluginInstance._instance.is_async:
            result.real_set_result = result.set_result
            result.set_result = lambda args: set_callback(*args)
            done_callback = lambda *args: result.real_set_result(args)
        return result

    @classmethod
    def _upload_multiple(cls, interactions, done_callback=None):
        for interaction in interactions:
            if interaction.index != -1:
                Logs.error("An interaction can only be uploaded once")
                return

        def set_callback(indices):
            for index, interaction in zip(indices, interactions):
                interaction.index = index
            if done_callback is not None:
                done_callback()

        id = PluginNetwork._instance.send(Messages.create_interactions, interactions, True)
        result = nanome.PluginInstance._save_callback(id, set_callback if done_callback else None)
        if done_callback is None and nanome.PluginInstance._instance.is_async:
            result.real_set_result = result.set_result
            result.set_result = lambda args: set_callback(*args)
            done_callback = lambda *args: result.real_set_result(args)
        return result

    def _destroy(self):
        PluginNetwork._instance.send(Messages.delete_interactions, [self.index], False)

    @classmethod
    def _destroy_multiple(cls, interactions):
        indices = [x.index for x in interactions]
        Logs.debug("Destroying interactions", indices)
        PluginNetwork._instance.send(Messages.delete_interactions, indices, False)

    @classmethod
    def _get_interactions(cls, args, done_callback):
        def set_callback(interactions):
            done_callback(interactions)

        id = PluginNetwork._instance.send(Messages.get_interactions, args, True)
        result = nanome.PluginInstance._save_callback(id, set_callback if done_callback else None)
        if done_callback is None and nanome.PluginInstance._instance.is_async:
            result.real_set_result = result.set_result
            result.set_result = lambda args: set_callback(*args)
            done_callback = lambda *args: result.real_set_result(args)
        return result

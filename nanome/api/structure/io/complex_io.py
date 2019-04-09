from nanome._internal._addon import _Addon
from nanome._internal._structure._io import _pdb, _sdf, _mmcif

class ComplexIO(_Addon):
    def __init__(self, base_object=None):
        _Addon.__init__(self, base_object)

    def to_pdb(self, path, options = None):
        """
        | Saves the complex into a .pdb file

        :param path: Path to the file
        :param options: Save options
        :type path: str
        :type options: :class:`~nanome._internal._structure._io._pdb.save.Options`

        .. todo::
            Write a user-facing API for options, so they can be documented
        """

        _pdb.to_file(path, self.base_object, options)

    def from_pdb(self, path, options = None):
        """
        | Loads the complex from a .pdb file

        :param path: Path to the file
        :type path: str
        :return: The complex read from the file
        :rtype: :class:`~nanome.api.structure.complex.Complex`
        """

        content = _pdb.parse_file(path)
        return _pdb.structure(content)

    def to_sdf(self, path, options = None):
        """
        | Saves the complex into a .sdf file

        :param path: Path to the file
        :param options: Save options
        :type path: str
        :type options: :class:`~nanome._internal._structure._io._sdf.save.Options`

        .. todo::
            Write a user-facing API for options, so they can be documented
        """

        _sdf.to_file(path, self.base_object, options)

    def from_sdf(self, path, options = None):
        """
        | Loads the complex from a .sdf file

        :param path: Path to the file
        :type path: str
        :return: The complex read from the file
        :rtype: :class:`~nanome.api.structure.complex.Complex`
        """

        content = _sdf.parse_file(path)
        return _sdf.structure(content)

    def to_mmcif(self, path, options = None):
        """
        | Saves the complex into a .cif file

        :param path: Path to the file
        :param options: Save options
        :type path: str
        :type options: :class:`~nanome._internal._structure._io._mmcif.save.Options`

        .. todo::
            Write a user-facing API for options, so they can be documented
        """

        _mmcif.to_file(path, self.base_object, options)

    def from_mmcif(self, path, options = None):
        """
        | Loads the complex from a .cif file

        :param path: Path to the file
        :type path: str
        :return: The complex read from the file
        :rtype: :class:`~nanome.api.structure.complex.Complex`
        """

        content = _mmcif.parse_file(path)
        return _mmcif.structure(content)
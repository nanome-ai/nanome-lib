import nanome
from nanome._internal._addon import _Addon
from nanome._internal._structure._io import _pdb, _sdf, _mmcif

class ComplexIO(_Addon):
    PDBSaveOptions = nanome.util.complex_save_options.PDBSaveOptions
    SDFSaveOptions = nanome.util.complex_save_options.SDFSaveOptions
    MMCIFSaveOptions = nanome.util.complex_save_options.MMCIFSaveOptions

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

    def from_pdb(self, file = None, content = None):
        """
        | Loads the complex from a .pdb file

        :param path: Path to the file
        :type path: str
        :return: The complex read from the file
        :rtype: :class:`~nanome.api.structure.complex.Complex`
        """
        return self.__from_file(file, content, _pdb)

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

    def from_sdf(self, file = None, content = None):
        """
        | Loads the complex from a .sdf file

        :param path: Path to the file
        :type path: str
        :return: The complex read from the file
        :rtype: :class:`~nanome.api.structure.complex.Complex`
        """
        return self.__from_file(file, content, _sdf)

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

    def from_mmcif(self, file = None, content = None):
        """
        | Loads the complex from a .cif file

        :param path: Path to the file
        :type path: str
        :return: The complex read from the file
        :rtype: :class:`~nanome.api.structure.complex.Complex`
        """
        return self.__from_file(file, content, _mmcif)

    def __from_file(self, file, content, parser):
        if (file != None):
            result = parser.parse_file(file)
        elif(content != None):
            if (isinstance(content, str)):
                result = parser.parse_string(content)
            else:
                result = parser.parse_lines(content)
        else:
            raise ValueError("Cannot read from type None")
        return parser.structure(result)
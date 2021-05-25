import nanome
from nanome._internal._addon import _Addon
from nanome._internal._structure._io import _pdb, _sdf, _mmcif


class ComplexIO(_Addon):
    PDBSaveOptions = nanome.util.complex_save_options.PDBSaveOptions
    SDFSaveOptions = nanome.util.complex_save_options.SDFSaveOptions
    MMCIFSaveOptions = nanome.util.complex_save_options.MMCIFSaveOptions

    def __init__(self, base_object=None):
        _Addon.__init__(self, base_object)

    def to_pdb(self, path, options=None):
        """
        | Saves the complex into a .pdb file

        :param path: Path to the file
        :param options: Save options
        :type path: str
        :type options: :class:`~nanome.util.complex_save_options.PDBSaveOptions`
        """

        _pdb.to_file(path, self.base_object, options)

    def from_pdb(self, **kwargs):
        """
        | Loads the complex from a .pdb file

        :return: The complex read from the file
        :rtype: :class:`~nanome.structure.Complex`
        :param kwargs: See below
        :Keyword Arguments:
            *path* (:class:`str`)
                Path to the file containing the structure
            *file* (:class:`file`)
                Opened file containing the structure
            *lines* (list of :class:`str`)
                List of lines from the file
            *string* (:class:`str`)
                Contents of the file as a single string
        """
        return self.__from_file(kwargs, _pdb)

    def to_sdf(self, path, options=None):
        """
        | Saves the complex into a .sdf file

        :param path: Path to the file
        :param options: Save options
        :type path: str
        :type options: :class:`~nanome.util.complex_save_options.SDFSaveOptions`
        """

        _sdf.to_file(path, self.base_object, options)

    def from_sdf(self, **kwargs):
        """
        | Loads the complex from a .sdf file

        :return: The complex read from the file
        :rtype: :class:`~nanome.structure.Complex`
        :param kwargs: See below
        :Keyword Arguments:
            *path* (:class:`str`)
                Path to the file containing the structure
            *file* (:class:`file`)
                Opened file containing the structure
            *lines* (list of :class:`str`)
                List of lines from the file
            *string* (:class:`str`)
                Contents of the file as a single string
        """
        return self.__from_file(kwargs, _sdf)

    def to_mmcif(self, path, options=None):
        """
        | Saves the complex into a .cif file

        :param path: Path to the file
        :param options: Save options
        :type path: str
        :type options: :class:`~nanome.util.complex_save_options.MMCIFSaveOptions`
        """

        _mmcif.to_file(path, self.base_object, options)

    def from_mmcif(self, **kwargs):
        """
        | Loads the complex from a .cif file

        :return: The complex read from the file
        :rtype: :class:`~nanome.structure.Complex`
        :param kwargs: See below
        :Keyword Arguments:
            *path* (:class:`str`)
                Path to the file containing the structure
            *file* (:class:`file`)
                Opened file containing the structure
            *lines* (list of :class:`str`)
                List of lines from the file
            *string* (:class:`str`)
                Contents of the file as a single string
        """
        return self.__from_file(kwargs, _mmcif)

    def __from_file(self, kwargs, parser):
        if (len(kwargs) != 1):
            nanome.util.Logs.warning("Multiple args not supported. Ignoring extraneous arguments.")

        if ("path" in kwargs):
            path = kwargs["path"]
            with open(path) as f:
                lines = f.readlines()
        elif ("file" in kwargs):
            file = kwargs["file"]
            lines = file.readlines()
        elif ("lines" in kwargs):
            lines = kwargs["lines"]
        elif ("string" in kwargs):
            lines = kwargs["string"].splitlines()
        else:
            raise ValueError("No valid argument")
        content = parser.parse_lines(lines)
        return parser.structure(content)

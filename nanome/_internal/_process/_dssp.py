from nanome.util import Process, Logs
from nanome._internal._structure import _Complex, _Residue
from nanome._internal._structure._io import _pdb

import tempfile
import os
import stat
import sys
import traceback

if sys.platform.startswith("linux"):
    DSSP_PATH = os.path.join(os.path.dirname(__file__), '_external', '_dssp', 'dssp-linux')
    os.chmod(DSSP_PATH, 0o777)
elif sys.platform.startswith("win"):
    DSSP_PATH = os.path.join(os.path.dirname(__file__), '_external', '_dssp', 'dssp-3.0.0-win32.exe')
else:
    DSSP_PATH = None


class _Dssp():
    _types_coil = [' ', 'C', 'S', 'T']
    _types_sheet = ['B', 'E']
    _types_helix = ['G', 'H', 'I']

    def __init__(self, complex_list, callback):
        self.__complexes = complex_list
        self.__framed_complexes = [complex.convert_to_frames() for complex in complex_list]
        self.__callback = callback

    def _start(self):
        if DSSP_PATH == None:
            Logs.error("Unsupported platform, cannot call DSSP")
            self.__callback(self.__complexes)
            return

        self.__complex_idx = 0
        self.__molecule_idx = -1
        self.__input = tempfile.NamedTemporaryFile(delete=False, suffix='.pdb')
        self.__output = tempfile.NamedTemporaryFile(delete=False, suffix='.dssp')
        self.__current_complex_result = []

        self.__proc = Process()
        self.__proc.executable_path = DSSP_PATH
        self.__proc.args = ['-i', self.__input.name, '-o', self.__output.name]
        self.__proc.output_text = True
        self.__proc.on_error = self.__on_error
        self.__proc.on_done = self.__dssp_done

        self.__next()

    def __next(self):
        # Go to next molecule
        complex = self.__complexes[self.__complex_idx]
        framed_complex = self.__framed_complexes[self.__complex_idx]

        self.__molecule_idx += 1
        # first frame if conformer, all frames if in frames (may change)
        if self.__molecule_idx >= len(complex._molecules):
            self.__update_secondary_structure(complex)
            del self.__current_complex_result[:]
            self.__complex_idx += 1
            if self.__complex_idx >= len(self.__complexes):
                self.__done()
                return
            complex = self.__complexes[self.__complex_idx]
            framed_complex = self.__framed_complexes[self.__complex_idx]
            self.__molecule_idx = 0

        molecule = framed_complex._molecules[self.__molecule_idx]
        single_frame = _Complex._create()
        single_frame._add_molecule(molecule)
        _pdb.to_file(self.__input.name, single_frame)

        self.__proc.start()

    def __on_error(self, msg):
        Logs.warning("[DSSP]", msg)

    def __dssp_done(self, result_code):
        if result_code != 0:
            Logs.error("DSSP failed, code:", result_code)
            self.__callback(self.__complexes)
            return
        with open(self.__output.name) as f:
            lines = f.readlines()
        secondary = self.__parse_dssp(lines)
        Logs.debug(secondary)
        self.__current_complex_result.append(secondary)
        self.__next()

    def __parse_dssp(self, lines):
        result = []
        i = 0
        while i < len(lines):
            if lines[i][2] == '#':
                i += 1
                while i < len(lines) and len(lines[i]) > 0:
                    line = lines[i]
                    serial = ""
                    try:
                        serial = line[5:10].strip()
                        if serial == "":
                            i += 1
                            continue
                        structure_type = line[16:17]
                        chain = line[10:12].strip()
                        result.append((chain, int(serial), structure_type))
                    except:
                        Logs.warning("[DSSP] Parsing error on serial:", serial)
                        Logs.warning(traceback.format_exc())
                    i += 1
            i += 1
        return result

    def __update_secondary_structure(self, complex):
        molecules = complex._molecules
        if len(molecules) != len(self.__current_complex_result):
            Logs.debug("[DSSP] Complex", complex._name, ": Molecule count", len(molecules), "doesn't match DSSP count", len(self.__current_complex_result))
            return

        for i in range(len(self.__current_complex_result)):
            secondary = self.__current_complex_result[i]
            molecule = molecules[i]

            residues = dict()
            for chain in molecule._chains:
                residues[chain._name] = dict()
                for residue in chain._residues:
                    residues[chain._name][residue._serial] = residue
            for dssp_info in secondary:
                try:
                    chain = residues[dssp_info[0]]
                    residue = chain[dssp_info[1]]
                    structure_type = dssp_info[2]
                    if structure_type in _Dssp._types_coil:
                        residue._secondary_structure = _Residue.SecondaryStructure.Coil
                    elif structure_type in _Dssp._types_sheet:
                        residue._secondary_structure = _Residue.SecondaryStructure.Sheet
                    elif structure_type in _Dssp._types_helix:
                        residue._secondary_structure = _Residue.SecondaryStructure.Helix
                except:
                    Logs.debug("[DSSP] Key not found:", dssp_info[0], dssp_info[1], traceback.format_exc())

    def __done(self):
        self.__input.close()
        self.__output.close()
        os.remove(self.__input.name)
        os.remove(self.__output.name)
        self.__callback(self.__complexes)

from nanome.util import Process
from nanome._internal._structure import _Complex, _Bond
from nanome._internal._structure._io import _pdb, _sdf

import tempfile
import os


class _Bonding():
    def __init__(self, complex_list, callback):
        self.__complexes = complex_list
        self.__callback = callback

        atom_count = 0
        for complex in complex_list:
            atom_count += sum(1 for _ in complex.atoms)
        self.__fast_mode = atom_count > 20000

    def _start(self):
        self.__complex_idx = 0
        self.__molecule_idx = -1
        self.__input = tempfile.NamedTemporaryFile(delete=False, suffix='.pdb')
        self.__output = tempfile.NamedTemporaryFile(delete=False, suffix='.mol')
        self.__saved_complex = _Complex._create()

        self.__proc = Process()
        self.__proc.executable_path = 'obabel'
        self.__proc.args = ['BONDING', '-i', '"' + self.__input.name + '"', '"' + self.__output.name + '"']
        self.__proc.on_done = self.__bonding_done
        if self.__fast_mode:
            self.__proc.args.append('-f')

        self.__next()

    def __next(self):
        # Go to next molecule
        complex = self.__complexes[self.__complex_idx]
        self.__molecule_idx += 1
        if self.__molecule_idx >= len(complex._molecules):
            self.__complex_idx += 1
            if self.__complex_idx >= len(self.__complexes):
                self.__done()
                return
            complex = self.__complexes[self.__complex_idx]
            self.__molecule_idx = 0
        molecule = complex._molecules[self.__molecule_idx]

        self.__saved_complex._molecules.clear()
        self.__saved_complex._molecules.append(molecule)
        _pdb.to_file(self.__input.name, complex)

        self.__proc.start()

    def __bonding_done(self):
        with open(self.__output.name) as f:
            lines = f.readlines()
        content = _sdf.parse_lines(lines)
        result = parser.structure(content)
        self.__match_and_bond(result)
        self.__next()

    def __match_and_bond(self, bonding_result):
        atom_by_serial = dict()
        for residue in self.__saved_complex.residues:
            residue._bonds.clear()
            for atom in residue.atoms:
                atom._bonds.clear()
                atom_by_serial[atom._serial] = (atom, residue)

        for residue in bonding_result.residues:
            for bond in residue.bonds:
                serial1 = bond._atom1._serial
                serial2 = bond._atom2._serial
                if serial1 in atom_by_serial and serial2 in atom_by_serial:
                    atom1, residue1 = atom_by_serial[serial1]
                    atom2, residue2 = atom_by_serial[serial2]
                    new_bond = _Bond._create()
                    new_bond._kind = bond._kind
                    new_bond._atom1 = atom1
                    new_bond._atom2 = atom2
                    residue1._bonds.append(new_bond)

    def __done(self):
        self.__input.close()
        self.__output.close()
        os.remove(self.__input.name)
        os.remove(self.__output.name)
        self.__callback(self.__complexes)

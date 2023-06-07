from nanome._internal.structure import _Complex, _Bond
from nanome._internal.structure.io import pdb, sdf

import functools
import tempfile
import os
from distutils.spawn import find_executable
import logging

logger = logging.getLogger(__name__)


try:
    import asyncio
except ImportError:
    asyncio = False

NANOBABEL_PATH = find_executable('nanobabel')
OBABEL_PATH = find_executable('obabel')


class Bonding():

    def __init__(self, plugin, complex_list, callback=None, fast_mode=None):
        self.__complexes = complex_list
        self.__callback = callback
        self.__future = None
        self.__input = None
        self.__output = None
        self.dir = tempfile.TemporaryDirectory()

        if asyncio and plugin.is_async:
            loop = asyncio.get_event_loop()
            future = loop.create_future()
            self.__future = future

        atom_count = 0
        if fast_mode is None:
            for complex in complex_list:
                atom_count += sum(atom._conformer_count for atom in complex.atoms)
            self.__fast_mode = atom_count > 20000
        else:
            self.__fast_mode = fast_mode

    def start(self):
        self.processes = []
        for comp in self.__complexes:
            comp.convert_to_frames()
            input_file = tempfile.NamedTemporaryFile(delete=False, dir=self.dir.name, suffix='.pdb')
            input_filename = input_file.name
            output_file = tempfile.NamedTemporaryFile(delete=False, dir=self.dir.name, suffix='.mol')
            output_filename = output_file.name
            comp.io.to_pdb(input_file.name)
            callback = functools.partial(self._handle_results_and_run_next_process, output_filename, comp)
            proc = self.setup_process(input_filename, output_filename, callback)
            self.processes.append(proc)
        current_proc = self.processes.pop(-1)
        current_proc.start()

    def setup_process(self, input_file, output_file, callback_fn):
        from nanome.util import Process
        proc = Process()
        proc.output_text = True
        proc.on_error = self.__on_error
        proc.on_done = callback_fn
        if NANOBABEL_PATH:
            proc.label = 'nanobabel'
            proc.executable_path = NANOBABEL_PATH
            proc.args += ['bonding', '-i', input_file, '-o', output_file]
        elif OBABEL_PATH:
            proc.label = 'obabel'
            proc.executable_path = OBABEL_PATH
            proc.args += ['-ipdb', input_file, '-osdf', '-O' + output_file]
        else:
            logger.error("No bonding package found.")

        if self.__fast_mode:
            proc.args.append('-f')
        return proc

    def old_start(self):
        from nanome.util import Process
        if len(self.__complexes) == 0:
            self.__done()
            return self.__future

        self.__complex_idx = 0
        self.__molecule_idx = -1
        self.__input = tempfile.NamedTemporaryFile(delete=False, dir=self.dir, suffix='.pdb')
        self.__output = tempfile.NamedTemporaryFile(delete=False, dir=self.dir, suffix='.mol')

        self.__proc = Process()
        self.__proc.output_text = True
        self.__proc.on_error = self.__on_error
        self.__proc.on_done = self._handle_results_and_run_next_process

        if NANOBABEL_PATH:
            self.__proc.label = 'nanobabel'
            self.__proc.executable_path = NANOBABEL_PATH
            self.__proc.args += ['bonding', '-i', self.__input.name, '-o', self.__output.name]
        elif OBABEL_PATH:
            self.__proc.label = 'obabel'
            self.__proc.executable_path = OBABEL_PATH
            self.__proc.args += ['-ipdb', self.__input.name, '-osdf', '-O' + self.__output.name]
        else:
            logger.error("No bonding package found.")

        if self.__fast_mode:
            self.__proc.args.append('-f')

        self.__next()
        return self.__future

    def __next(self):
        # Go to next molecule
        complex = self.__complexes[self.__complex_idx]
        framed_complex = self.__framed_complexes[self.__complex_idx]

        self.__molecule_idx += 1
        if self.__molecule_idx >= len(framed_complex._molecules):
            self.__complex_idx += 1
            if self.__complex_idx >= len(self.__complexes):
                self.__done()
                return

            complex = self.__complexes[self.__complex_idx]
            framed_complex = self.__framed_complexes[self.__complex_idx]
            self.__molecule_idx = 0

        self.__saved_complex = complex
        self.__saved_is_conformer = len(complex._molecules) == 1

        molecule = framed_complex._molecules[self.__molecule_idx]
        single_frame = _Complex._create()
        single_frame._add_molecule(molecule)
        pdb.to_file(self.__input.name, single_frame)

        self.__proc.start()

    def __on_error(self, msg):
        if "molecule converted" not in msg:
            logger.warning("[Bond Generation] " + msg)

    def _handle_results_and_run_next_process(self, output_file, initial_comp, result_code):
        if result_code == -1:
            logger.error("Couldn't execute nanobabel or openbabel to generate bonds. Is one installed?")
            self.__done()
            return
        with open(output_file) as f:
            lines = f.readlines()
        content = sdf.parse_lines(lines)
        result_comp = sdf.structure(content)
        self._match_and_bond(initial_comp, result_comp)
        # self.__next()

    @classmethod
    def _match_and_bond(cls, unbonded_comp, bonded_comp):
        assert len(list(unbonded_comp.atoms)) == len(list(bonded_comp.atoms))
        # make one to one mapping of atoms based on position
        bonded_serial_to_unbonded_atom = dict()

        def sort_lambda(atm):
            return atm.position.unpack()
        sorted_unbonded_atoms = sorted(list(unbonded_comp.atoms), key=sort_lambda)
        sorted_bonded_atoms = sorted(list(bonded_comp.atoms), key=sort_lambda)

        for initial_atom, bonded_atom in zip(sorted_unbonded_atoms, sorted_bonded_atoms):
            assert initial_atom.position == bonded_atom.position
            bonded_serial_to_unbonded_atom[bonded_atom.serial] = initial_atom

        # make bonds for each atom in unbonded_comp
        for bond in bonded_comp.bonds:
            serial1 = bond._atom1._serial
            serial2 = bond._atom2._serial

            if serial1 > serial2:
                serial1, serial2 = serial2, serial1

            if serial1 in bonded_serial_to_unbonded_atom and serial2 in bonded_serial_to_unbonded_atom:
                atom1 = bonded_serial_to_unbonded_atom[serial1]
                atom2 = bonded_serial_to_unbonded_atom[serial2]
                residue = atom1._residue

                new_bond = None
                for old_bond in atom1.bonds:
                    if old_bond._atom2 == atom2:
                        new_bond = old_bond
                        break

                if new_bond is None:
                    new_bond = _Bond._create()
                    new_bond._kind = bond._kind
                    new_bond._atom1 = atom1
                    new_bond._atom2 = atom2
                    residue._add_bond(new_bond)

    def __match_and_bond(self, bonding_result):
        if self.__molecule_idx == 0:
            for atom in self.__saved_complex.atoms:
                del atom._bonds[:]
            for residue in self.__saved_complex.residues:
                del residue._bonds[:]

        if self.__molecule_idx == 0 or not self.__saved_is_conformer:
            self.__atom_by_serial = dict()
            molecule = self.__saved_complex._molecules[self.__molecule_idx]

            # obabel removes gaps in atom serials going from pdb to sdf
            # we need to remove the gaps before matching output to saved complex
            atom_serial = 1
            for atom in molecule.atoms:
                self.__atom_by_serial[atom_serial] = atom
                atom_serial += 1

        for bond in bonding_result.bonds:
            serial1 = bond._atom1._serial
            serial2 = bond._atom2._serial

            if serial1 > serial2:
                serial1, serial2 = serial2, serial1

            if serial1 in self.__atom_by_serial and serial2 in self.__atom_by_serial:
                atom1 = self.__atom_by_serial[serial1]
                atom2 = self.__atom_by_serial[serial2]
                residue = atom1._residue

                new_bond = None
                for old_bond in atom1.bonds:
                    if old_bond._atom2 == atom2:
                        new_bond = old_bond
                        break

                if new_bond is None:
                    new_bond = _Bond._create()
                    new_bond._kind = bond._kind

                    if self.__saved_is_conformer:
                        conformer_count = atom1.conformer_count
                        new_bond._kinds = [new_bond._kind] * conformer_count
                        new_bond._in_conformer = [False] * conformer_count

                    new_bond._atom1 = atom1
                    new_bond._atom2 = atom2
                    residue._add_bond(new_bond)

                if self.__saved_is_conformer:
                    new_bond._in_conformer[self.__molecule_idx] = True

    def __done(self):
        if self.__input is not None:
            self.__input.close()
            os.remove(self.__input.name)

        if self.__output is not None:
            self.__output.close()
            os.remove(self.__output.name)

        if self.__callback is not None:
            self.__callback(self.__complexes)

        if self.__future is not None:
            self.__future.set_result(self.__complexes)

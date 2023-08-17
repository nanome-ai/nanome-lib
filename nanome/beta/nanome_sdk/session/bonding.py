import logging
import subprocess
import tempfile
from nanome.api.structure import Bond, Complex
from nanome.util import Logs
from distutils.spawn import find_executable


logger = logging.getLogger(__name__)


class Bonding:

    @classmethod
    def start(cls, complex_list):
        """Start the bonding process."""
        for input_comp in complex_list:
            # is_conformer = len(next(input_comp.atoms).in_conformer) > 1
            # input_comp.convert_to_frames()
            input_file = tempfile.NamedTemporaryFile(suffix='.pdb', delete=False)
            output_file = tempfile.NamedTemporaryFile(suffix='.mol', delete=False)
            input_comp.io.to_pdb(input_file.name)
            popen = cls.start_bonding_process(input_file.name, output_file.name)
            popen.wait()
            bonded_comp = Complex.io.from_sdf(path=output_file.name)
            assert len(list(input_comp.molecules)) == len(list(bonded_comp.molecules))
            for input_mol, bonded_mol in zip(input_comp.molecules, bonded_comp.molecules):
                assert sum(1 for _ in input_mol.atoms) == sum(1 for _ in bonded_mol.atoms)
                cls._match_and_bond(input_mol, bonded_mol)

    @classmethod
    def start_bonding_process(cls, input_filepath: str, output_filepath: str):
        NANOBABEL_PATH = find_executable('nanobabel')
        OBABEL_PATH = find_executable('obabel')
        Logs.debug(f'OBABEL_PATH={OBABEL_PATH}')

        cmd = []
        if OBABEL_PATH:
            cmd = [OBABEL_PATH, '-ipdb', input_filepath, '-osdf', '-O' + output_filepath]
        elif NANOBABEL_PATH:
            cmd = [NANOBABEL_PATH, 'bonding', '-i', input_filepath, '-o', output_filepath]
        if cmd:
            proc = subprocess.Popen(cmd)
            return proc
        else:
            raise Exception("Bonding program not found.")

    @staticmethod
    def _match_and_bond(unbonded_mol, bonded_mol):
        """Copy all the bonds from bonded_mol to unbonded_mol."""
        # Serial numbering may be different between the two complexes,
        # so make mapping of atoms based on position
        bonded_serial_to_unbonded_atom = dict()

        def sort_key(atm): return str(atm.position.unpack())  # noqa: E731
        sorted_unbonded_atoms = sorted(list(unbonded_mol.atoms), key=sort_key)
        sorted_bonded_atoms = sorted(list(bonded_mol.atoms), key=sort_key)
        for unbonded_atom, bonded_atom in zip(sorted_unbonded_atoms, sorted_bonded_atoms):
            assert unbonded_atom.position.unpack() == bonded_atom.position.unpack()
            bonded_serial_to_unbonded_atom[bonded_atom.serial] = unbonded_atom

        # make bonds for each atom in unbonded_mol
        for bond in bonded_mol.bonds:
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
                    new_bond = Bond._create()
                    new_bond._kind = bond._kind
                    new_bond._atom1 = atom1
                    new_bond._atom2 = atom2
                    residue._add_bond(new_bond)

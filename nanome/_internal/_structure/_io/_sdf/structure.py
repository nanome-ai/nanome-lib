from nanome.util import Vector3
from nanome._internal._structure import _Complex, _Molecule, _Chain, _Residue, _Bond, _Atom
from .content import Content

def structure(content):
    # type: (Content) -> Complex
    complex = _Complex._create()
    for model in content.models:
        complex._molecules.append(structure_molecule(model))
    complex.molecular._remarks = {}
    return complex


def structure_molecule(model):
    # type: (Content.Model) -> Molecule
    molecule = _Molecule._create()
    molecule.molecular._name = model.name

    chain = _Chain._create()
    chain.molecular._name = "S"
    molecule._chains.append(chain)
    residue = _Residue._create()
    residue.molecular._name = "SDF"
    residue.molecular.serial = 1
    chain._residues.append(residue)
    atoms_by_serial = {}

    for catom in model.atoms:
        atom = _Atom._create()
        atom.molecular._symbol = catom.symbol
        atom.molecular._serial = catom.serial
        atom.molecular._position = Vector3(catom.x, catom.y, catom.z)
        atom.molecular._name = catom.symbol
        atom.molecular._is_het = True
        residue._atoms.append(atom)
        atoms_by_serial[atom.molecular._serial] = atom
    for cbond in model.bonds:
        if cbond.serial_atom1 in atoms_by_serial and cbond.serial_atom2 in atoms_by_serial:
            bond = _Bond._create()
            bond._atom1 = atoms_by_serial[cbond.serial_atom1]
            bond._atom2 = atoms_by_serial[cbond.serial_atom2]
            bond.molecular._kind = cbond.bond_order
            residue._bonds.append(bond)
    molecule.molecular._associated = model._associated
    return molecule

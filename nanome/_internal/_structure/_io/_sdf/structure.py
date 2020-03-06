from nanome.util import enums
from nanome.util import Vector3
from nanome._internal._structure import _Complex, _Molecule, _Chain, _Residue, _Bond, _Atom
from .content import Content

def structure(content):
    # type: (Content) -> Complex
    complex = _Complex._create()
    for model in content.models:
        complex._add_molecule(structure_molecule(model))
    complex._remarks = {}
    return complex._convert_to_conformers()


def structure_molecule(model):
    # type: (Content.Model) -> Molecule
    molecule = _Molecule._create()
    molecule._name = model.name

    chain = _Chain._create()
    chain._name = "S"
    molecule._add_chain(chain)
    residue = _Residue._create()
    residue._name = "SDF"
    residue._type = residue._name
    residue.serial = 1
    chain._add_residue(residue)
    atoms_by_serial = {}

    for catom in model.atoms:
        atom = _Atom._create()
        atom._symbol = catom.symbol
        atom._serial = catom.serial
        atom._position = Vector3(catom.x, catom.y, catom.z)
        atom._name = catom.symbol
        atom._is_het = True
        atom._formal_charge = catom.charge
        residue._add_atom(atom)
        atoms_by_serial[atom._serial] = atom
    for cbond in model.bonds:
        if cbond.serial_atom1 in atoms_by_serial and cbond.serial_atom2 in atoms_by_serial:
            bond = _Bond._create()
            bond._atom1 = atoms_by_serial[cbond.serial_atom1]
            bond._atom2 = atoms_by_serial[cbond.serial_atom2]
            bond._kind = enums.Kind.safe_cast(cbond.bond_order)
            residue._add_bond(bond)
    molecule._associated = model._associated
    return molecule

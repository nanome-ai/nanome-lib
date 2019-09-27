def _deep_copy_complex(complex):
    return __deep_copy_complex(complex, {})

def _deep_copy_molecule(molecule):
    return __deep_copy_molecule(molecule, {})

def _deep_copy_chain(chain):
    return __deep_copy_chain(chain, {})

def _deep_copy_residue(residue):
    return __deep_copy_residue(residue, {})

def __deep_copy_complex(complex, bond_set):
    new_complex = complex._shallow_copy()
    for molecule in complex._molecules:
        new_complex._add_molecule(__deep_copy_molecule(molecule, bond_set))
    return new_complex

def __deep_copy_molecule(molecule, bond_set):
    new_molecule = molecule._shallow_copy()
    for chain in molecule._chains:
        new_molecule._add_chain(__deep_copy_chain(chain, bond_set))
    return new_molecule

def __deep_copy_chain(chain, bond_set):
    new_chain = chain._shallow_copy()
    for residue in chain._residues:
        new_chain._add_residue(__deep_copy_residue(residue, bond_set))
    return new_chain
def __deep_copy_residue(residue, bond_set):
    new_residue = residue._shallow_copy()
    for bond in residue._bonds:
        new_bond = __no_dup_copy_bond(bond, bond_set)
        new_residue.add_bond(new_bond)
    for atom in residue._atoms:
        new_atom = atom._shallow_copy()
        new_residue._add_atom(new_atom)
        for bond in atom._bonds:
            new_bond = __no_dup_copy_bond(bond, bond_set)
            if bond._atom1 == atom:
                new_bond._atom1 = new_atom
            else:
                new_bond._atom2 = new_atom
    return new_residue

def __no_dup_copy_bond(bond, bond_set):
    if bond not in bond_set:
        bond_set[bond] = bond._shallow_copy()
    return bond_set[bond]

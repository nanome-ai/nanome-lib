def _deep_copy_complex(complex):
    return __deep_copy_complex(complex, {})

def _deep_copy_molecule(molecule):
    return __deep_copy_molecule(molecule, {})

def _deep_copy_chain(chain):
    return __deep_copy_chain(chain, {})

def _deep_copy_residue(residue):
    return __deep_copy_residue(residue, {})

def __deep_copy_complex(complex, atoms_by_index):
    new_complex = complex._shallow_copy()
    for molecule in complex._molecules:
        new_complex._add_molecule(__deep_copy_molecule(molecule, atoms_by_index))
    return new_complex

def __deep_copy_molecule(molecule, atoms_by_index):
    new_molecule = molecule._shallow_copy()
    for chain in molecule._chains:
        new_molecule._add_chain(__deep_copy_chain(chain, atoms_by_index))
    return new_molecule

def __deep_copy_chain(chain, atoms_by_index):
    new_chain = chain._shallow_copy()
    for residue in chain._residues:
        new_chain._add_residue(__deep_copy_residue(residue, atoms_by_index))
    return new_chain

def __deep_copy_residue(residue, atoms_by_index):
    new_residue = residue._shallow_copy()
    for atom in residue._atoms:
        new_atom = __no_dup_copy_atom(atom, atoms_by_index)
        new_residue._add_atom(new_atom)
    for bond in residue._bonds:
        new_bond = bond._shallow_copy()
        new_bond._atom1 = __no_dup_copy_atom(bond._atom1, atoms_by_index)
        new_bond._atom2 = __no_dup_copy_atom(bond._atom2, atoms_by_index)
        new_residue.add_bond(new_bond)
    return new_residue

def __no_dup_copy_atom(atom, atoms_by_index):
    id = atom._unique_identifier
    if id not in atoms_by_index:
        atoms_by_index[id] = atom._shallow_copy()
    return atoms_by_index[id]

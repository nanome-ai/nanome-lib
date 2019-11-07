def _deep_copy_complex(complex):
    return __deep_copy_complex(complex, {})

def _deep_copy_molecule(molecule, conformer_number = None):
    return __deep_copy_molecule(molecule, {}, conformer_number)

def _deep_copy_chain(chain, conformer_number = None):
    return __deep_copy_chain(chain, {}, conformer_number)

def _deep_copy_residue(residue, conformer_number = None):
    return __deep_copy_residue(residue, {}, conformer_number)

def __deep_copy_complex(complex, bond_set):
    new_molecules = []
    for molecule in complex._molecules:
        new_molecule = __deep_copy_molecule(molecule, bond_set, None)
        if new_molecule != None:
            new_molecules = __list_with(new_molecules, new_molecule)
    new_complex = complex._shallow_copy()
    new_complex._set_molecules(new_molecules)
    return new_complex

def __deep_copy_molecule(molecule, bond_set, conformer_number):
    new_chains = None
    for chain in molecule._chains:
        new_chain = __deep_copy_chain(chain, bond_set, conformer_number)
        if new_chain != None:
            new_chains = __list_with(new_chains, new_chain)
    if new_chains != None:
        new_molecule = molecule._shallow_copy(conformer_number)
        new_molecule._set_chains(new_chains)
        return new_molecule
    return molecule._shallow_copy(conformer_number)

def __deep_copy_chain(chain, bond_set, conformer_number):
    new_residues = None
    for residue in chain._residues:
        new_residue = __deep_copy_residue(residue, bond_set, conformer_number)
        if new_residue != None:
            new_residues = __list_with(new_residues, new_residue)
    if new_residues != None:
        new_chain = chain._shallow_copy(conformer_number)
        new_chain._set_residues(new_residues)
        return new_chain
    if conformer_number is None: #the structure organically has no residues
        return chain._shallow_copy(conformer_number)
    return None

def __deep_copy_residue(residue, bond_set, conformer_number):
    new_bonds = None
    new_atoms = None
    for bond in residue._bonds:
        if conformer_number is None or bond._in_conformer[conformer_number]:
            new_bond = __no_dup_copy_bond(bond, bond_set, conformer_number)
            new_bonds = __list_with(new_bonds, new_bond)
    for atom in residue._atoms:
        if conformer_number is None or atom._in_conformer[conformer_number]:
            new_atom = atom._shallow_copy(conformer_number)
            new_atoms = __list_with(new_atoms, new_atom)
        for bond in atom._bonds:
            if conformer_number is None or bond._in_conformer[conformer_number]:
                new_bond = __no_dup_copy_bond(bond, bond_set, conformer_number)
                if bond._atom1 == atom:
                    new_bond._atom1 = new_atom
                else:
                    new_bond._atom2 = new_atom
    if new_atoms != None:
        new_residue = residue._shallow_copy(conformer_number)
        new_residue._set_atoms(new_atoms)
        if new_bonds != None:
            new_residue._set_bonds(new_bonds)
        return new_residue
    if conformer_number is None: #the structure organically has no atoms or bonds
        return residue._shallow_copy(conformer_number)
    return None

def __no_dup_copy_bond(bond, bond_set, conformer_number):
    pair = (bond, conformer_number)
    if pair not in bond_set:
        bond_set[pair] = bond._shallow_copy(conformer_number)
    return bond_set[pair]

def __list_with(var, val):
    if (var == None):
        var = []
    var.append(val)
    return var
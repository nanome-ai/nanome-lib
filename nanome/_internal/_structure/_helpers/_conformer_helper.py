import hashlib, copy
from nanome.util import StringBuilder
s_ConformersDisabled = False #Nanome.Core.Config.getBool("mol-conformers-disabled", "false")
s_ConformersAlways = False #Nanome.Core.Config.getBool("mol-conformers-always", "false")

def _delete_atoms(atoms):
    for atom in atoms:
        atom.name == "DELETED"
        atom._residue._atoms.remove(atom)
    del atoms[:]

def _delete_bonds(bonds):
    for bond in bonds:
        bond._atom1 = None
        bond._atom2 = None
        bond._residue.remove_bond(bond)
    del bonds[:]

def _delete_residues(residues):
    for residue in residues:
        residue._chain._remove_residue(residue)
    del residues[:]

def _delete_chains(chains):
    for chain in chains:
        chain._molecule._remove_chain(chain)
    del chains[:]

#disabled hashing until I can find a fast algorithm
def _get_hash_code(str):
    return str #int(hashlib.sha256(str.encode('utf-8')).hexdigest(), 16)

def convert_to_frames(complex): #Data.Complex -> Data.Complex
    deleted_atoms = []
    deleted_bonds = []
    deleted_residues = []
    deleted_chains = []
    new_complex = complex._shallow_copy()
    for molecule in complex._molecules:
        if molecule._conformer_count > 1:
            count = molecule._conformer_count
            for i in range(count):
                new_molecule = molecule._deep_copy()
                new_molecule._names = [molecule._names[i]]
                new_molecule._associateds = [molecule._associateds[i]]
                for new_chain in new_molecule._chains:
                    for new_residue in new_chain._residues:
                        for new_atom in new_residue._atoms:
                            if not new_atom._exists[i]:
                                deleted_atoms.append(new_atom)
                            new_atom._positions = [new_atom._positions[i]]
                            new_atom._exists = [True]
                        _delete_atoms(deleted_atoms)                        
                        for new_bond in new_residue._bonds:
                            if not new_bond._exists[i]:
                                deleted_bonds.append(new_bond)
                            new_bond._kinds = [new_bond._kinds[i]]
                            new_bond._exists = [True]
                        _delete_bonds(deleted_bonds)
                        if len(new_residue._atoms) == 0:
                            deleted_residues.append(new_residue)
                    _delete_residues(deleted_residues)
                    if len(new_chain._residues) == 0:
                        deleted_chains.append(new_chain)
                _delete_chains(deleted_chains)
                new_molecule._conformer_count = 1
                new_complex._add_molecule(new_molecule)
        else:
            new_complex._add_molecule(molecule._deep_copy())
    for atom in new_complex.atoms:
        if (atom._bonds == None):
            print("WTF2")
    return new_complex

def convert_to_conformers(complex, force_conformer = None): #Data.Complex -> Data.Complex
    if force_conformer == None:
        force_conformer = s_ConformersAlways
    # Maybe conformers are disabled
    if s_ConformersDisabled:
        return complex
    # How much are we talking about here
    count = len(complex._molecules)
    # No mutliple frames, nothing to do
    if count <= 1:
        return complex
    # Collect count of first molecule
    molecule_index = 0
    chain_total_count = 0
    residue_total_count = 0
    atom_total_count = 0
    bond_total_count = 0
    # Create molecular container
    new_complex = complex._shallow_copy() #Data.Complex
    new_molecule = complex._molecules[0]._shallow_copy() # Data.Molecule
    # Group structures by their hash
    new_chains = {}
    new_residues = {}
    new_atoms = {}
    new_bonds = {}
    # Computation stores
    sb = StringBuilder()
    names_dictionary = {}
    atoms_dictionary = {}
    # Get ready
    new_complex._add_molecule(new_molecule)
    new_molecule._conformer_count = len(complex._molecules)

    # Loop over all frames
    for molecule in complex._molecules:
        # Meta informations
        new_molecule._names[molecule_index] = molecule._name
        new_molecule._associateds[molecule_index] = molecule._associated
        # Loop over all chains
        for chain in molecule._chains:
            # Lookup or create chain with hash
            hash_chain = _get_chain_hash(sb, chain)
            new_chain = None
            if hash_chain in new_chains:
                new_chain = new_chains[hash_chain]
            else:
                new_chain = chain._shallow_copy()
                new_molecule._add_chain(new_chain)
                new_chains[hash_chain] = new_chain
            # Loop over all residues
            for residue in chain._residues:
                # Lookup or create chain with hash
                hash_residue = _get_residue_hash(sb, residue)
                new_residue = None
                if hash_residue in new_residues:
                    new_residue = new_residues[hash_residue]
                else:
                    new_residue = residue._shallow_copy()
                    new_chain._add_residue(new_residue)
                    new_residues[hash_residue] = new_residue
                # Cleanup
                names_dictionary.clear()

                for atom in residue._atoms:
                    name_hash = _get_hash_code(atom.name)
                    off = 0
                    if name_hash in names_dictionary:
                        off = names_dictionary[name_hash]
                    names_dictionary[name_hash] = off
                    # Lookup or create atom with hash
                    hash_atom = _get_atom_hash(sb, atom, off)
                    new_atom = None
                    if hash_atom in new_atoms:
                        new_atom = new_atoms[hash_atom]
                    else:
                        new_atom = atom._shallow_copy()
                        new_atom._exists = [None]*new_molecule._conformer_count # replace with append algorithm at the end
                        new_atom._positions = [None]*new_molecule._conformer_count
                        new_residue._add_atom(new_atom)
                        if off > 1:
                            new_atom.name = new_atom.name + str(off)
                        new_atom.serial = len(new_residue._atoms)
                        new_atoms[hash_atom] = new_atom
                    # Update current conformer
                    new_atom._exists[molecule_index] = True
                    new_atom._positions[molecule_index] = atom.position
                    # Save
                    atoms_dictionary[atom._unique_identifier] = (hash_atom, new_atom)
                    atom_total_count+=1
                residue_total_count+=1
            chain_total_count+=1

        for bond in molecule.bonds:
            atom_info_1 = atoms_dictionary[bond._atom1._unique_identifier]
            atom_info_2 = atoms_dictionary[bond._atom2._unique_identifier]

            # Lookup the parent residue
            residue = bond._parent
            hash_residue = _get_residue_hash(sb, residue)
            new_residue = new_residues[hash_residue]

            hash_bond = _get_bond_hash(sb, bond, atom_info_1[0], atom_info_2[0])
            new_bond = None
            if hash_bond in new_bonds:
                new_bond = new_bonds[hash_bond]
                # print(_get_residue_hash(sb, new_bond._parent) == _get_residue_hash(sb, bond._parent))
            else:
                new_bond = bond._shallow_copy()
                new_bond._exists = [None]*new_molecule._conformer_count # replace with append algorithm at the end
                new_bond._kinds = [None]*new_molecule._conformer_count
                new_residue._add_bond(new_bond)
                new_bonds[hash_bond] = new_bond
            # Update current conformer
            new_bond._exists[molecule_index] = True
            new_bond._kinds[molecule_index] = bond.kind
            # Count bonds
            bond_total_count+=1

        for atom in molecule.atoms:
            for bond in molecule.bonds:
                atom_info_1 = atoms_dictionary[bond._atom1._unique_identifier]#Tuple<int, Data.Atom>
                atom_info_2 = atoms_dictionary[bond._atom2._unique_identifier]#Tuple<int, Data.Atom>

                # Lookup the parent residue
                residue = bond._parent
                hash_residue = _get_residue_hash(sb, residue)
                new_residue = new_residues[hash_residue]

                hash_bond = _get_bond_hash(sb, bond, atom_info_1[0], atom_info_2[0])
                new_bond = new_bonds[hash_bond]
                if atom == bond._atom1:
                    new_bond._atom1 = atom_info_1[1]
                else:
                    new_bond._atom2 = atom_info_2[1]

        # Molecule idx
        molecule_index+=1
    # Important decision to make, is everything suited for a trajectories?
    if not force_conformer:
        # Gather important information of the conversion
        is_very_big_chains = chain_total_count > 1 #bool
        is_very_big_residues = residue_total_count > 10 #bool
        is_very_big_atoms = atom_total_count > 10000 # So basically im not very smol #bool
        is_very_big_bonds = bond_total_count > 20000 #bool
        chain_similarity_ratio = float(chain_total_count) / float(count) / float(len(new_chains)) #float
        residue_similarity_ratio = float(residue_total_count) / float(count) / float(len(new_residues)) #float
        atom_similarity_ratio = float(atom_total_count) / float(count) / float(len(new_atoms)) #float
        bond_similarity_ratio = float(bond_total_count) / float(count) / float(len(new_bonds)) #float
        is_chain_similar_enough = chain_similarity_ratio > 0.85 #bool
        is_residue_similar_enough = residue_similarity_ratio > 0.85 #bool
        is_atom_similar_enough = atom_similarity_ratio > 0.85 #bool
        is_bond_similar_enough = bond_similarity_ratio > 0.85 #bool
        # Debug # Keeping for short term debug
        # from nanome.util import Logs
        # Logs.debug("Conformers", "RESULTS")
        # Logs.debug("Conformers", "count", count)
        # Logs.debug("Conformers", "is_very_big_chains", is_very_big_chains)
        # Logs.debug("Conformers", "is_very_big_residues", is_very_big_residues)
        # Logs.debug("Conformers", "is_very_big_atoms", is_very_big_atoms)
        # Logs.debug("Conformers", "is_very_big_bonds", is_very_big_bonds)
        # Logs.debug("Conformers", "chain_similarity_ratio", chain_similarity_ratio)
        # Logs.debug("Conformers", "residue_similarity_ratio", residue_similarity_ratio)
        # Logs.debug("Conformers", "atom_similarity_ratio", atom_similarity_ratio)
        # Logs.debug("Conformers", "bond_similarity_ratio", bond_similarity_ratio)
        # Logs.debug("Conformers", "is_chain_similar_enough", is_chain_similar_enough)
        # Logs.debug("Conformers", "is_residue_similar_enough", is_residue_similar_enough)
        # Logs.debug("Conformers", "is_atom_similar_enough", is_atom_similar_enough)
        # Logs.debug("Conformers", "is_bond_similar_enough", is_bond_similar_enough)
        # Logs.debug("Conformers", "chain_total_count", chain_total_count)
        # Logs.debug("Conformers", "residue_total_count", residue_total_count)
        # Logs.debug("Conformers", "atom_total_count", atom_total_count)
        # Logs.debug("Conformers", "bond_total_count", bond_total_count)
        # Logs.debug("Conformers", "new_chains.Count", len(new_chains))
        # Logs.debug("Conformers", "new_residues.Count", len(new_residues))
        # Logs.debug("Conformers", "new_atoms.Count", len(new_atoms))
        # Logs.debug("Conformers", "new_bonds.Count", len(new_bonds))
        
        # Cancel conversion if not suited
        if is_very_big_chains and not is_chain_similar_enough:
            return complex
        if is_very_big_residues and not is_residue_similar_enough:
            return complex
        if is_very_big_atoms and not is_atom_similar_enough:
            return complex
        if is_very_big_bonds and not is_bond_similar_enough:
            return complex
    # Otherwise let's start grabbing the data
    return new_complex

def _get_chain_hash(sb, chain): #StringBuilder, Data.Chain -> int
    return _get_hash_code(chain.name)

def _get_residue_hash(sb, residue): #StringBuilder, Data.Residue -> int
    sb.clear()
    sb.append(residue._serial)
    sb.append(":")
    sb.append(residue._name)
    sb.append(":")
    sb.append(residue._chain._name)
    return _get_hash_code(sb.to_string())

def _get_atom_hash(sb, atom, off): #StringBuilder, Data.Atom, int -> int
    sb.clear()
    sb.append(atom._symbol)
    sb.append(":")
    sb.append(atom._name)
    sb.append(":")
    sb.append(atom._is_het)
    sb.append(":")
    sb.append(off)
    sb.append(":")
    sb.append(atom._residue._serial)
    sb.append(":")
    sb.append(atom._residue._name)
    sb.append(":")
    sb.append(atom._residue._chain._name)
    return _get_hash_code(sb.to_string())

def _get_bond_hash(sb, bond, atom1, atom2): #StringBuilder, Data.Bond, int, int -> int
    sb.clear()
    sb.append(atom1)
    sb.append(":")
    sb.append(atom2)
    sb.append(":")
    sb.append(bond._residue._serial)
    sb.append(":")
    sb.append(bond._residue._name)
    sb.append(":")
    sb.append(bond._chain._name)
    return _get_hash_code(sb.to_string())
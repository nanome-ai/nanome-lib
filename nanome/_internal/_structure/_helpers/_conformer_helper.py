import hashlib
import copy
from nanome.util import StringBuilder, Vector3, enums
s_ConformersDisabled = False  # Nanome.Core.Config.getBool("mol-conformers-disabled", "false")
s_ConformersAlways = False  # Nanome.Core.Config.getBool("mol-conformers-always", "false")


def _get_hash_code(string):
    return hash(string)


def convert_to_frames(complex, old_to_new_atoms=None):  # Data.Complex -> Data.Complex
    new_complex = complex._shallow_copy()
    for molecule in complex._molecules:
        count = molecule._conformer_count
        for i in range(count):
            new_complex.add_molecule(molecule._deep_copy(i, old_to_new_atoms))
    return new_complex


def convert_to_conformers(complex, force_conformer=None):  # Data.Complex -> Data.Complex
    frame_count = len(complex._molecules)
    # Maybe conformers are disabled
    if frame_count <= 1 or s_ConformersDisabled:
        return complex._deep_copy()
    # Collect count of first molecule
    molecule_index = 0
    chain_total_count = 0
    residue_total_count = 0
    atom_total_count = 0
    bond_total_count = 0
    # Create molecular container
    new_complex = complex._shallow_copy()  # Data.Complex
    new_complex._current_frame = 0
    new_molecule = complex._molecules[0]._shallow_copy()  # Data.Molecule
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
                    off += 1
                    names_dictionary[name_hash] = off
                    # Lookup or create atom with hash
                    hash_atom = _get_atom_hash(sb, atom, off)
                    new_atom = None
                    if hash_atom in new_atoms:
                        new_atom = new_atoms[hash_atom]
                    else:
                        new_atom = atom._shallow_copy()
                        new_atom._in_conformer = [False] * new_molecule._conformer_count
                        new_atom._positions = [Vector3()] * new_molecule._conformer_count
                        new_residue._add_atom(new_atom)
                        if off > 1:
                            new_atom.name = new_atom.name + str(off)
                        new_atoms[hash_atom] = new_atom
                        new_atom.serial = len(new_atoms)
                    # Update current conformer
                    new_atom._in_conformer[molecule_index] = True
                    new_atom._positions[molecule_index] = atom.position.get_copy()
                    # Save
                    atoms_dictionary[atom._unique_identifier] = (hash_atom, new_atom)
                    atom_total_count += 1
                residue_total_count += 1
            chain_total_count += 1

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
            else:
                new_bond = bond._shallow_copy()
                new_bond._in_conformer = [False] * new_molecule._conformer_count
                new_bond._kinds = [enums.Kind.CovalentSingle] * new_molecule._conformer_count
                new_residue._add_bond(new_bond)
                new_bonds[hash_bond] = new_bond
            # Update current conformer
            new_bond._in_conformer[molecule_index] = True
            new_bond._kinds[molecule_index] = bond.kind
            # Count bonds
            bond_total_count += 1

        for atom in molecule.atoms:
            for bond in atom.bonds:
                atom_info_1 = atoms_dictionary[bond._atom1._unique_identifier]
                atom_info_2 = atoms_dictionary[bond._atom2._unique_identifier]

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
        molecule_index += 1
    if force_conformer == None:
        force_conformer = s_ConformersAlways
    # Important decision to make, is everything suited for a trajectories?
    if not force_conformer:
        # Gather important information of the conversion
        is_very_big_chains = chain_total_count > 1
        is_very_big_residues = residue_total_count > 10
        is_very_big_atoms = atom_total_count > 10000
        is_very_big_bonds = bond_total_count > 20000
        if len(new_chains) == 0:
            chain_similarity_ratio = 1
        else:
            chain_similarity_ratio = float(chain_total_count) / float(frame_count) / float(len(new_chains))
        if len(new_residues) == 0:
            residue_similarity_ratio = 1
        else:
            residue_similarity_ratio = float(residue_total_count) / float(frame_count) / float(len(new_residues))
        if len(new_atoms) == 0:
            atom_similarity_ratio = 1
        else:
            atom_similarity_ratio = float(atom_total_count) / float(frame_count) / float(len(new_atoms))
        if len(new_bonds) == 0:
            bond_similarity_ratio = 1
        else:
            bond_similarity_ratio = float(bond_total_count) / float(frame_count) / float(len(new_bonds))
        is_chain_similar_enough = chain_similarity_ratio > 0.85
        is_residue_similar_enough = residue_similarity_ratio > 0.85
        is_atom_similar_enough = atom_similarity_ratio > 0.85
        is_bond_similar_enough = bond_similarity_ratio > 0.85
        # Cancel conversion if not suited
        if is_very_big_chains and not is_chain_similar_enough:
            return complex._deep_copy()
        if is_very_big_residues and not is_residue_similar_enough:
            return complex._deep_copy()
        if is_very_big_atoms and not is_atom_similar_enough:
            return complex._deep_copy()
        if is_very_big_bonds and not is_bond_similar_enough:
            return complex._deep_copy()
    # Otherwise let's start grabbing the data
    return new_complex


def _get_chain_hash(sb, chain):  # StringBuilder, Data.Chain -> int
    return _get_hash_code(chain.name)


def _get_residue_hash(sb, residue):  # StringBuilder, Data.Residue -> int
    sb.clear()
    sb.append(residue._serial)
    sb.append_string(residue._name)
    sb.append_string(residue._chain._name)
    return _get_hash_code(sb.to_string(":"))


def _get_atom_hash(sb, atom, off):  # StringBuilder, Data.Atom, int -> int
    sb.clear()
    sb.append(atom._symbol)
    sb.append_string(atom._name)
    sb.append(atom._is_het)
    sb.append(off)
    sb.append(atom._residue._serial)
    sb.append_string(atom._residue._name)
    sb.append_string(atom._residue._chain._name)
    return _get_hash_code(sb.to_string(":"))


def _get_bond_hash(sb, bond, atom1, atom2):  # StringBuilder, Data.Bond, int, int -> int
    sb.clear()
    sb.append(atom1)
    sb.append(atom2)
    sb.append(bond._residue._serial)
    sb.append_string(bond._residue._name)
    sb.append_string(bond._chain._name)
    return _get_hash_code(sb.to_string(":"))

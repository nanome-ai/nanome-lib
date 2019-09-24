import hashlib, copy
from ... import _structure as struct
s_ConformersDisabled = False #Nanome.Core.Config.getBool("mol-conformers-disabled", "false")
s_ConformersAlways = False #Nanome.Core.Config.getBool("mol-conformers-always", "false")

class StringBuilder:
    def __init__(self):
        self.los =[]
    def append(self, s):
        self.los.append(str(s))
    def to_string(self):
        return self.get()
    def get(self):
        return "".join(self.los)
    def clear(self):
        self.los.clear()

def delete_atom(atom):
    for bond in atom._bonds:
        delete_bond(bond)
    atom._residue._atoms.remove(atom)

def delete_bond(bond):
    bond._atom1._bonds.remove(bond)
    bond._atom2._bonds.remove(bond)
    bond._residue._bonds.remove(bond)

def get_hash_code(str):
    return int(hashlib.sha256(str.encode('utf-8')).hexdigest(), 16)

def convert_to_frames(complex): #Data.Complex -> Data.Complex
    deleted_atoms = [] #new List<Data.Atom>()
    deleted_bonds = [] #new List<Data.Bond>()
    new_complex = complex._shallow_copy() # Data.Complex
    for molecule in complex._molecules:
        if molecule._conformer_count > 1:
            count = molecule._conformer_count
            for i in range(count):
                new_molecule = molecule._deep_copy()
                new_molecule._names = [molecule._names[i]]
                new_molecule._associateds = [molecule._associateds[i]]
                for new_chain in new_molecule._chains:
                    for new_residue in new_chain._residues:
                        deleted_atoms.clear()
                        deleted_bonds.clear()
                        for new_atom in new_residue._atoms:
                            if not new_atom._exists[i]:
                                deleted_atoms.append(new_atom)
                            new_atom._positions = [new_atom._positions[i]]
                            new_atom._exists = [True]
                        for new_bond in new_residue._bonds:
                            if not new_bond._exists[i]:
                                deleted_bonds.append(new_bond)
                            new_bond._kinds = [new_bond._kinds[i]]
                        for deleted_bond in deleted_bonds:
                            delete_bond(deleted_bond)
                        for deleted_atom in deleted_atoms:
                            delete_atom(deleted_atom)
                new_complex._add_molecule(new_molecule)
        else:
            new_complex._add_molecule(molecule._deep_copy())
    return new_complex

def convert_all_to_conformers(complexes): #List<Data.Complex -> List<Data.Complex>
    results = [] #List<Data.Complex> 
    for complex in complexes:
        results.append(convert_to_conformers(complex))
    return results

def convert_to_conformers(complex): #Data.Complex -> Data.Complex
    # Maybe conformers are disabled
    if s_ConformersDisabled:
        return complex
    # How much are we talking about here
    count = len(complex._molecules) #int
    # No mutliple frames, nothing to do
    if count <= 1:
        return complex
    # Collect count of first molecule
    molecule_index = 0
    chain_total_count = 0
    residue_total_count = 0
    atom_total_count = 0
    bont_total_count = 0
    # Create molecular container
    new_complex = complex._shallow_copy() #Data.Complex
    new_molecule = complex._molecules[0]._shallow_copy() # Data.Molecule
    # Group structures by their hash
    new_chains = {} #Dictionary<int, Data.Chain> 
    new_residues = {} #Dictionary<int, Data.Residue> 
    new_atoms = {} #Dictionary<int, Data.Atom> 
    new_bonds = {} #Dictionary<int, Data.Bond> 
    # Computation stores
    sb = StringBuilder() #StringBuilder
    names_dictionary = {} #Dictionary<int, int> 
    atoms_dictionary = {} #Dictionary<int, Tuple<int, Data.Atom>> 
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
            hash_chain = get_chain_hash(sb, chain) #int
            new_chain = None #Data.Chain
            if hash_chain in new_chains:
                new_chain = new_chains[hash_chain]
            else:
                new_chain = chain._shallow_copy()
                new_molecule._add_chain(new_chain)
                new_chains[hash_chain] = new_chain
            # Loop over all residues
            for residue in chain._residues:
                # Lookup or create chain with hash
                hash_residue = get_residue_hash(sb, residue) #int
                new_residue = None #Data.Residue
                if hash_residue in new_residues:
                    new_residue = new_residues[hash_residue]
                else:
                    new_residue = residue._shallow_copy()
                    new_chain._add_residue(new_residue)
                    new_residues[hash_residue] = new_residue
                # Cleanup
                names_dictionary.clear()
                # Loop over all atoms
                for atom in residue._atoms:
                    name_hash = get_hash_code(atom.name) #int
                    off = 0 #int
                    if name_hash in names_dictionary:
                        off = names_dictionary[name_hash]
                    off+=1
                    names_dictionary[name_hash] = off
                    # Lookup or create chain with hash
                    hash_atom = get_atom_hash(sb, atom, off) #int
                    new_atom = None #Data.Atom
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
                    # Loop over all bonds
                    for bond in atom._bonds:
                        atom_info_1 = None#Tuple<int, Data.Atom>
                        atom_info_2 = None#Tuple<int, Data.Atom>
                        found1 = bond._atom1._unique_identifier in atoms_dictionary
                        if found1:
                            atom_info_1 = atoms_dictionary[bond._atom1._unique_identifier]
                        found2 = bond._atom2._unique_identifier in atoms_dictionary
                        if found2:
                            atom_info_2 = atoms_dictionary[bond._atom2._unique_identifier]
                        if found1 and found2:
                            hash_bond = get_bond_hash(sb, bond, atom_info_1[0], atom_info_2[1]) #int
                            new_bond = None #Data.Bond
                            if hash_bond in new_bonds:
                                new_bond = new_bonds[hash_bond]
                            else:
                                new_bond = bond._shallow_copy()
                                new_bond._exists = [None]*new_molecule._conformer_count # replace with append algorithm at the end
                                new_bond._kinds = [None]*new_molecule._conformer_count                                
                                new_bond._atom1 = atom_info_1[1]
                                new_bond._atom2 = atom_info_2[1]
                                new_residue._add_bond(new_bond)
                                new_bonds[hash_bond] = new_bond
                            # Update current conformer
                            new_bond._exists[molecule_index] = True
                            new_bond._kinds[molecule_index] = bond.kind
                            # Count bonds
                            bont_total_count+=1
                    # Count atoms
                    atom_total_count+=1
                # Count residues
                residue_total_count+=1
            # Count chains
            chain_total_count+=1
        # Molecule idx
        molecule_index+=1
    # Important decision to make, is everything suited for a trajectories?
    if not s_ConformersAlways:
        # Gather important information of the conversion
        is_very_big_chains = chain_total_count > 1 #bool
        is_very_big_residues = residue_total_count > 10 #bool
        is_very_big_atoms = atom_total_count > 10000 # So basically im not very smol #bool
        is_very_big_bonds = bont_total_count > 20000 #bool
        chain_similarity_ratio = float(chain_total_count) / float(count) / float(len(new_chains)) #float
        residue_similarity_ratio = float(residue_total_count) / float(count) / float(len(new_residues)) #float
        atom_similarity_ratio = float(atom_total_count) / float(count) / float(len(new_atoms)) #float
        bond_similarity_ratio = float(bont_total_count) / float(count) / float(len(new_bonds)) #float
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
        # Logs.debug("Conformers", "bont_total_count", bont_total_count)
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

def get_chain_hash(sb, chain): #StringBuilder, Data.Chain -> int
    return get_hash_code(chain.name)

def get_residue_hash(sb, residue): #StringBuilder, Data.Residue -> int
    sb.clear()
    sb.append(residue.serial)
    sb.append(":")
    sb.append(residue.name)
    sb.append(":")
    sb.append(residue.chain.name)
    return get_hash_code(sb.to_string())

def get_atom_hash(sb, atom, off): #StringBuilder, Data.Atom, int -> int
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
    return get_hash_code(sb.to_string())

def get_bond_hash(sb, bond, atom1, atom2): #StringBuilder, Data.Bond, int, int -> int
    sb.clear()
    sb.append(atom1)
    sb.append(":")
    sb.append(atom2)
    return get_hash_code(sb.to_string())

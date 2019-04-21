from nanome.util import Vector3
from nanome._internal._structure import _Complex, _Molecule, _Chain, _Residue, _Bond, _Atom
from .content import Content

def structure(content):
    num_molecules = max(content.model_count, 1)
    atoms_by_molecule = []
    for i in range(num_molecules):
        atoms_by_molecule.append([])

    for ratom in content.atoms:
        atoms_by_molecule[ratom.model_number - 1].append(ratom)
    complex = _Complex._create()
    complex.molecular._remarks = content._remarks
    for i in range(num_molecules):
        molecule = structure_molecule(atoms_by_molecule[i], content.compnds)
        molecule.molecular._name = str(i)
        complex._molecules.append(molecule)
    # Done
    return complex
        
         
def structure_molecule(atoms, compnds):
    # All structured infos
    all_residues = {} #<string, Residue>
    all_chains = {} #<string, Chain>
    all_atoms = {} #<string, Atom>
    # Read all atoms
    for ratom in atoms:
        atom = _Atom._create()
        atom.molecular._symbol = ratom.element_symbol
        atom.molecular._serial = ratom.atom_serial_number
        atom.molecular._name = ratom.atom_name
        #atom.molecular.alts = ratom.atom_alternate_location
        atom.molecular._occupancy = ratom.occupancy
        atom.molecular._bfactor = ratom.bfactor
        #atom.molecular.charge = ratom.atom_charge
        atom.molecular._position = Vector3(ratom.atom_x, ratom.atom_y, ratom.atom_z)
        atom.molecular._is_het = ratom.is_het_atom
        atom_id = ratom.chain_identifier + ":" + str(ratom.residue_serial_number) + ":" + ratom.atom_name + ":" + str(ratom.atom_serial_number)
        if not atom_id in all_atoms:
            residue_id = ratom.chain_identifier + ":" + str(ratom.residue_serial_number) + ":" + ratom.segment_identifier
            if not residue_id in all_residues:
                residue = _Residue._create()
                residue.molecular._name = ratom.residue_name
                residue.molecular._serial = ratom.residue_serial_number
                # residue.insertion_code = ratom.residue_insertion_code
                all_residues[residue_id] = residue
                chain_id = ratom.chain_identifier
                if ratom.is_het_atom:
                    chain_id = "H" + chain_id
                if not chain_id in all_chains:
                    chain = _Chain._create()
                    chain.molecular._name = chain_id
                    all_chains[chain_id] = chain
                all_chains[chain_id]._residues.append(residue)
            all_residues[residue_id]._atoms.append(atom)
            all_atoms[atom_id] = atom
    # Final molecule
    molecule = _Molecule._create()
    # Assemble molecule contents
    for chain in all_chains:
        molecule._chains.append(all_chains[chain])
    # Done
    return molecule
        

    


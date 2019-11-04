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
    complex._remarks = content._remarks
    for i in range(num_molecules):
        molecule = structure_molecule(atoms_by_molecule[i], content.compnds)
        molecule._name = str(i)
        complex._add_molecule(molecule)
    # Done
    return complex._convert_to_conformers()
        
         
def structure_molecule(atoms, compnds):
    # All structured infos
    all_residues = {} #<string, Residue>
    all_chains = {} #<string, Chain>
    all_atoms = {} #<string, Atom>
    # Read all atoms
    for ratom in atoms:
        atom = _Atom._create()
        atom._symbol = ratom.element_symbol
        atom._serial = ratom.atom_serial_number
        atom._name = ratom.atom_name
        #atom.alts = ratom.atom_alternate_location
        atom._occupancy = ratom.occupancy
        atom._bfactor = ratom.bfactor
        #atom.charge = ratom.atom_charge
        atom._position = Vector3(ratom.atom_x, ratom.atom_y, ratom.atom_z)
        atom._is_het = ratom.is_het_atom
        atom_id = ratom.chain_identifier + ":" + str(ratom.residue_serial_number) + ":" + ratom.atom_name + ":" + str(ratom.atom_serial_number)
        if not atom_id in all_atoms:
            residue_id = ratom.chain_identifier + ":" + str(ratom.residue_serial_number) + ":" + ratom.segment_identifier
            if not residue_id in all_residues:
                residue = _Residue._create()
                residue._name = ratom.residue_name
                residue._type = residue._name
                residue._serial = ratom.residue_serial_number
                # residue.insertion_code = ratom.residue_insertion_code
                all_residues[residue_id] = residue
                chain_id = ratom.chain_identifier
                if ratom.is_het_atom:
                    chain_id = "H" + chain_id
                if not chain_id in all_chains:
                    chain = _Chain._create()
                    chain._name = chain_id
                    all_chains[chain_id] = chain
                all_chains[chain_id]._add_residue(residue)
            all_residues[residue_id]._add_atom(atom)
            all_atoms[atom_id] = atom
    # Final molecule
    molecule = _Molecule._create()
    # Assemble molecule contents
    for chain in all_chains:
        molecule._add_chain(all_chains[chain])
    # Done
    return molecule
        

    


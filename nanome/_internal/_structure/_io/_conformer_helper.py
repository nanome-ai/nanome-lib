import hashlib, copy
from ... import _structure as struct
s_ConformersDisabled = False #Nanome.Core.Config.getBool("mol-conformers-disabled", "false")
s_ConformersAlways = False #Nanome.Core.Config.getBool("mol-conformers-always", "false")

class StringBuilder:
    los = []
    def append(self, str):
        StringBuilder.los.append(str)
    def ToString(self):
        return self.get()
    def get(self):
        return "".join(StringBuilder.los)

def delete_atom(atom):
    for bond in atom._bonds:
        delete_bond(bond)
    atom._residue._atoms.remove(atom)

def delete_bond(bond):
    bond._atom1._bonds.remove(bond)
    bond._atom2._bonds.remove(bond)
    bond._residue._bonds.remove(bond)

def get_hash_code(str):
    return hashlib.sha1(str)

def ConvertToFrames(complex): #Data.Complex -> Data.Complex
    deletedAtoms = [] #new List<Data.Atom>()
    deletedBonds = [] #new List<Data.Bond>()
    newComplex = complex._shallow_copy(True) # Data.Complex
    for molecule in complex._molecules:
        if molecule.__conformer_count > 1:
            count = molecule.__conformer_count
            for i in range(count):
                newMolecule = molecule._deep_copy(True, True)
                newMolecule._names = [molecule._names[i]]
                newMolecule._associateds = [molecule._associateds[i]]
                for newChain in newMolecule._chains:
                    for newResidue in newChain._residues:
                        deletedAtoms.clear()
                        deletedBonds.clear()
                        for newAtom in newResidue._atoms:
                            if not newAtom._exists[i]:
                                deletedAtoms.append(newAtom)
                            newAtom._positions = [newAtom.positions[i]]
                            newAtom._exists = [True]
                        for newBond in newResidue._bonds:
                            if not newBond._exists[i]:
                                deletedBonds.append(newBond)
                            newBond.kinds = [newBond.kinds[i]]
                        for deletedBond in deletedBonds:
                            delete_bond(deletedBond)
                        for deletedAtom in deletedAtoms:
                            delete_atom(deletedAtom)
                newComplex._add_molecule(newMolecule)
        else:
            newComplex._add_molecule(molecule._deep_copy(True, False))
    return newComplex

def ConvertAllToConformers(complexes): #List<Data.Complex -> List<Data.Complex>
    results = [] #List<Data.Complex> 
    for complex in complexes:
        results.append(ConvertToConformers(complex))
    return results

def ConvertToConformers(complex): #Data.Complex -> Data.Complex
    # Maybe conformers are disabled
    if s_ConformersDisabled:
        return complex
    # How much are we talking about here
    count = len(complex._molecules.count) #int
    # No mutliple frames, nothing to do
    if count <= 1:
        return complex
    # Collect count of first molecule
    moleculeIndex = 0
    chainTotalCount = 0
    residueTotalCount = 0
    atomTotalCount = 0
    bondTotalCount = 0
    # Create molecular container
    newComplex = complex.ShallowCopy(True) #Data.Complex
    newMolecule = complex._molecules[0].ShallowCopy(True) # Data.Molecule
    # Group structures by their hash
    newChains = {} #Dictionary<int, Data.Chain> 
    newResidues = {} #Dictionary<int, Data.Residue> 
    newAtoms = {} #Dictionary<int, Data.Atom> 
    newBonds = {} #Dictionary<int, Data.Bond> 
    # Computation stores
    sb = StringBuilder() #StringBuilder
    names = {} #Dictionary<int, int> 
    atoms = {} #Dictionary<int, Tuple<int, Data.Atom>> 
    # Get ready
    newComplex._add_molecule(newMolecule)
    # Loop over all frames
    for molecule in complex._molecules:
        # Meta informations
        newMolecule._names[moleculeIndex] = molecule.name
        newMolecule._associateds[moleculeIndex] = molecule.associated
        # Loop over all chains
        for chain in molecule._chains:
            # Lookup or create chain with hash
            hashChain = GetChainHash(sb, chain) #int
            newChain = None #Data.Chain
            if hashChain in newChains:
                newChain = newChains[hashChain]
            else:
                newChain = chain.ShallowCopy(True)
                newMolecule._add_chain(newChain)
                newChains[hashChain] = newChain
            # Loop over all residues
            for residue in chain._residues:
                # Lookup or create chain with hash
                hashResidue = GetResidueHash(sb, residue) #int
                newResidue = None #Data.Residue
                if hashResidue in newResidues:
                    newResidue = newResidues[hashResidue]
                else:
                    newResidue = residue.ShallowCopy(True)
                    newChain._add_residue(newResidue)
                    newResidues[hashResidue] = newResidue
                # Cleanup
                names.clear()
                # Loop over all atoms
                for atom in residue._atoms:
                    name = get_hash_code(atom.name) #int
                    off = 0 #int
                    if name in names:
                        off = names[name]
                    off+=1
                    names[name] = off
                    # Lookup or create chain with hash
                    hashAtom = GetAtomHash(sb, atom, off) #int
                    newAtom = None #Data.Atom
                    if hashAtom in newAtoms:
                        newAtom = newAtoms[hashAtom]
                    else:
                        newAtom = atom.ShallowCopy(True, False)
                        newResidue._add_atom(newAtom)
                        if off > 1:
                            newAtom.name = newAtom.name + off
                        newAtom.serial = len(newResidue._atoms)
                        newAtoms[hashAtom] = newAtom
                    # Update current conformer
                    newAtom._exists[moleculeIndex] = True
                    newAtom._positions[moleculeIndex] = atom.position()
                    # Save
                    atoms[atom.index] = (hashAtom, newAtom)
                    # Loop over all bonds
                    for bond in atom._bonds:
                        atomInfo1 = None#Tuple<int, Data.Atom>
                        atomInfo2 = None#Tuple<int, Data.Atom>
                        found1 = bond.atom1.index in atoms
                        if found1:
                            atomInfo1 = atoms[bond.atom1.index]
                        found2 = bond.atom1.index in atoms
                        if found2:
                            atomInfo2 = atoms[bond.atom2.index]
                        if found1 and found2:
                            hashBond = GetBondHash(sb, bond, atomInfo1.Item1, atomInfo2.Item1) #int
                            newBond = None #Data.Bond
                            if hashBond in newBonds:
                                newBond = hashBond
                            else:
                                newBond = bond.ShallowCopy(atomInfo1.Item2, atomInfo2.Item2, True, False)
                                newResidue._add_bond(newBond)
                                newBonds[hashBond] = newBond
                            # Update current conformer
                            newBond._exists[moleculeIndex] = True
                            newBond._orders[moleculeIndex] = bond.kind
                            # Count bonds
                            bondTotalCount+=1
                    # Count atoms
                    atomTotalCount+=1
                # Count residues
                residueTotalCount+=1
            # Count chains
            chainTotalCount+=1
        # Molecule idx
        moleculeIndex+=1
    # Important decision to make, is everything suited for a trajectories?
    if not s_ConformersAlways:
        # Gather important information of the conversion
        isVeryBigChains = chainTotalCount > 1 #bool
        isVeryBigResidues = residueTotalCount > 10 #bool
        isVeryBigAtoms = atomTotalCount > 10000 # So basically im not very smol #bool
        isVeryBigBonds = bondTotalCount > 20000 #bool
        chainSimilarityRatio = float(chainTotalCount) / float(count) / float(len(newChains)) #float
        residueSimilarityRatio = float(residueTotalCount) / float(count) / float(len(newResidues)) #float
        atomSimilarityRatio = float(atomTotalCount) / float(count) / float(len(newAtoms)) #float
        bondSimilarityRatio = float(bondTotalCount) / float(count) / float(len(newBonds)) #float
        isChainSimilarEnough = chainSimilarityRatio > 0.85 #bool
        isResidueSimilarEnough = residueSimilarityRatio > 0.85 #bool
        isAtomSimilarEnough = atomSimilarityRatio > 0.85 #bool
        isBondSimilarEnough = bondSimilarityRatio > 0.85 #bool
        # Debug # Keeping for short term debug
        #Logs.debugOnChannel("Conformers", "RESULTS")
        #Logs.debugOnChannel("Conformers", "count", count)
        #Logs.debugOnChannel("Conformers", "isVeryBigChains", isVeryBigChains)
        #Logs.debugOnChannel("Conformers", "isVeryBigResidues", isVeryBigResidues)
        #Logs.debugOnChannel("Conformers", "isVeryBigAtoms", isVeryBigAtoms)
        #Logs.debugOnChannel("Conformers", "isVeryBigBonds", isVeryBigBonds)
        #Logs.debugOnChannel("Conformers", "chainSimilarityRatio", chainSimilarityRatio)
        #Logs.debugOnChannel("Conformers", "residueSimilarityRatio", residueSimilarityRatio)
        #Logs.debugOnChannel("Conformers", "atomSimilarityRatio", atomSimilarityRatio)
        #Logs.debugOnChannel("Conformers", "bondSimilarityRatio", bondSimilarityRatio)
        #Logs.debugOnChannel("Conformers", "isChainSimilarEnough", isChainSimilarEnough)
        #Logs.debugOnChannel("Conformers", "isResidueSimilarEnough", isResidueSimilarEnough)
        #Logs.debugOnChannel("Conformers", "isAtomSimilarEnough", isAtomSimilarEnough)
        #Logs.debugOnChannel("Conformers", "isBondSimilarEnough", isBondSimilarEnough)
        #Logs.debugOnChannel("Conformers", "chainTotalCount", chainTotalCount)
        #Logs.debugOnChannel("Conformers", "residueTotalCount", residueTotalCount)
        #Logs.debugOnChannel("Conformers", "atomTotalCount", atomTotalCount)
        #Logs.debugOnChannel("Conformers", "bondTotalCount", bondTotalCount)
        #Logs.debugOnChannel("Conformers", "newChains.Count", newChains.Count)
        #Logs.debugOnChannel("Conformers", "newResidues.Count", newResidues.Count)
        #Logs.debugOnChannel("Conformers", "newAtoms.Count", newAtoms.Count)
        #Logs.debugOnChannel("Conformers", "newBonds.Count", newBonds.Count)
        
        # Cancel conversion if not suited
        if isVeryBigChains and not isChainSimilarEnough:
            return complex
        if isVeryBigResidues and not isResidueSimilarEnough:
            return complex
        if isVeryBigAtoms and not isAtomSimilarEnough:
            return complex
        if isVeryBigBonds and not isBondSimilarEnough:
            return complex
    # Otherwise let's start grabbing the data
    return newComplex

def GetChainHash(sb, chain): #StringBuilder, Data.Chain -> int
    return get_hash_code(chain.name)

def GetResidueHash(sb, residue): #StringBuilder, Data.Residue -> int
    sb.Length = 0
    sb.Append(residue.serial)
    sb.Append(":")
    sb.Append(residue.name)
    sb.Append(":")
    sb.Append(residue.chain.name)
    return get_hash_code(sb.ToString())

def GetAtomHash(sb, atom, off): #StringBuilder, Data.Atom, int -> int
    sb.Length = 0
    sb.Append(atom._symbol)
    sb.Append(":")
    sb.Append(atom.name)
    sb.Append(":")
    sb.Append(atom.isHet)
    sb.Append(":")
    sb.Append(off)
    sb.Append(":")
    sb.Append(atom.residue.serial)
    sb.Append(":")
    sb.Append(atom.residue.name)
    sb.Append(":")
    sb.Append(atom.residue.chain.name)
    return get_hash_code(sb.ToString())

def GetBondHash(sb, bond, atom1, atom2): #StringBuilder, Data.Bond, int, int -> int
    sb.Length = 0
    sb.Append(atom1)
    sb.Append(":")
    sb.Append(atom2)
    return get_hash_code(sb.ToString())

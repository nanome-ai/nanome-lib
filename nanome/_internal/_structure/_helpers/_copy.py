    public static class Convert
    {

        def _ToDataDeep(this Live.Complex complex, bool includeMeta, bool includeConformer:
            return complex.ToDataDeep(new Dictionary<long, Data.Atom>(), includeMeta, includeConformer)
        def _ToDataDeep(this Live.Molecule molecule, bool includeMeta, bool includeConformer:
            return molecule.ToDataDeep(new Dictionary<long, Data.Atom>(), includeMeta, includeConformer)
        def _ToDataDeep(this Live.Chain chain, bool includeMeta, bool includeConformer:
            return chain.ToDataDeep(new Dictionary<long, Data.Atom>(), includeMeta, includeConformer)
        def _ToDataDeep(this Live.Residue residue, bool includeMeta, bool includeConformer:
            return residue.ToDataDeep(new Dictionary<long, Data.Atom>(), includeMeta, includeConformer)

        def __ToDataDeep(this Live.Complex complex, Dictionary<long, Data.Atom> atomsbyIndex, bool includeMeta, bool includeConformer:
            Data.Complex newComplex = complex.ToDataShallow(includeMeta)
            foreach (Live.Molecule molecule in complex.GetMolecules():
                newComplex.Add(molecule.ToDataDeep(atomsbyIndex, includeMeta, includeConformer))
            return newComplex
        def __ToDataDeep(this Live.Molecule molecule, Dictionary<long, Data.Atom> atomsbyIndex, bool includeMeta, bool includeConformer:
            Data.Molecule newMolecule = molecule.ToDataShallow(includeMeta, includeConformer)
            foreach (Live.Chain chain in molecule.GetChains():
                newMolecule.Add(chain.ToDataDeep(atomsbyIndex, includeMeta, includeConformer))
            return newMolecule
        def __ToDataDeep(this Live.Chain chain, Dictionary<long, Data.Atom> atomsbyIndex, bool includeMeta, bool includeConformer:
            Data.Chain newChain = chain.ToDataShallow(includeMeta)
            foreach (Live.Residue residue in chain.GetResidues():
                newChain.Add(residue.ToDataDeep(atomsbyIndex, includeMeta, includeConformer))
            return newChain
        def __ToDataDeep(this Live.Residue residue, Dictionary<long, Data.Atom> atomsbyIndex, bool includeMeta, bool includeConformer:
            Data.Residue newResidue = residue.ToDataShallow(includeMeta)
            foreach (Live.Atom atom in residue.GetAtoms():
                Data.Atom newAtom = atom.ToDataShallow(includeMeta, includeConformer)
                atomsbyIndex[atom.index] = newAtom
                newResidue.Add(newAtom)
                foreach (Live.Bond bond in atom.GetBonds():
                    Data.Atom newAtom1 = null
                    Data.Atom newAtom2 = null
                    if (atomsbyIndex.TryGetValue(bond.atom1.index, out newAtom1)
                        && atomsbyIndex.TryGetValue(bond.atom2.index, out newAtom2):
                        newResidue.Add(bond.ToDataShallow(newAtom1, newAtom2, includeMeta, includeConformer))
            return newResidue

        def _ToDataShallow(this Live.Complex complex, bool includeMeta:
            Data.Complex newComplex = new Data.Complex()
            newComplex.name = complex.GetBaseName()
            newComplex.indexTag = complex.GetIndexTag()
            newComplex.splitTag = complex.GetSplitTag()
            foreach (string key in complex.GetRemarkKeys():
                newComplex.remarks.Add(key, complex.GetRemark(key))
            if (includeMeta:
                newComplex.meta.Copy(complex)
            return newComplex

        def _ToDataShallow(this Live.Molecule molecule, bool includeMeta, bool includeConformer:
            Data.Molecule newMolecule = new Data.Molecule()
            newMolecule.name = molecule.GetName()
            foreach (string key in molecule.GetAssociatedKeys():
                newMolecule.associated.Add(key, molecule.GetAssociatedData(key))
            if (includeMeta:
                newMolecule.meta.Copy(molecule)
            if (includeConformer && molecule.GetConformerEnabled():
                newMolecule.conformer = new Conformer.Molecule(molecule)
            return newMolecule

        def _ToDataShallow(this Live.Chain chain, bool includeMeta:
            Data.Chain newChain = new Data.Chain()
            newChain.name = chain.GetName()
            if (includeMeta:
                newChain.meta.Copy(chain)
            return newChain

        def _ToDataShallow(this Live.Residue residue, bool includeMeta:
            Data.Residue newResidue = new Data.Residue()
            newResidue.SetData(residue.GetData())
            newResidue.serial = residue.GetSerial()
            newResidue.name = residue.GetName()
            newResidue.ss = residue.GetSecondaryStructure()
            if (includeMeta:
                newResidue.meta.Copy(residue)
            return newResidue

        def _ToDataShallow(this Live.Atom atom, bool includeMeta, bool includeConformer:
            Data.Atom newAtom = new Data.Atom()
            newAtom.SetElement(atom.GetElement())
            newAtom.serial = atom.GetSerial()
            newAtom.name = atom.GetName()
            newAtom.SetSciencePosition(atom.GetSciencePosition())
            newAtom.isHet = atom.GetIsHet()
            newAtom.occupancy = atom.GetOccupancy()
            newAtom.bfactor = atom.GetBFactor()
            newAtom.acceptor = atom.GetAcceptor()
            newAtom.donor = atom.GetDonor()
            if (includeMeta:
                newAtom.meta.Copy(atom)
            if (includeConformer && atom.molecule.GetConformerEnabled():
                newAtom.conformer = new Conformer.Atom(atom)
            return newAtom

        def _ToDataShallow(this Live.Bond bond, Data.Atom a1, Data.Atom a2, bool includeMeta, bool includeConformer:
            Data.Bond newBond = new Data.Bond(a1, a2)
            newBond.kind = bond.GetKind()
            if (includeMeta:
                newBond.meta.Copy(bond)
            if (includeConformer && bond.molecule.GetConformerEnabled():
                newBond.conformer = new Conformer.Bond(bond)
            return newBond
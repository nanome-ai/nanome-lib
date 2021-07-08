

class ComplexUtils:
    """Useful util functions for working with Complexes."""

    @staticmethod
    def align_to(complex, reference_complex):
        """Set complex position and rotation relative to reference_complex."""
        m = complex.get_complex_to_workspace_matrix()
        for atom in complex.atoms:
            atom.position = m * atom.position
        complex.old_position = complex.position
        complex.old_rotation = complex.rotation
        complex.position = reference_complex.position
        complex.rotation = reference_complex.rotation
        m = complex.get_workspace_to_complex_matrix()
        for atom in complex.atoms:
            atom.position = m * atom.position

    @staticmethod
    def combine_ligands(receptor, ligands):
        """Align ligand Complexes to receptor, and combine into one Complex."""
        from nanome.api.structure import Complex
        combined_ligands = Complex()
        combined_ligands.names = []
        for ligand in ligands:
            ComplexUtils.align_to(ligand, receptor)
            combined_ligands.names.append(ligand.full_name)
            for molecule in ligand.molecules:
                combined_ligands.add_molecule(molecule)
        return combined_ligands

    @staticmethod
    def convert_to_conformers(complexes):
        for i in range(len(complexes)):
            complex_index = complexes[i].index
            complexes[i] = complexes[i].convert_to_conformers()
            complexes[i].index = complex_index

    @staticmethod
    def convert_to_frames(complexes):
        for i in range(len(complexes)):
            complex_index = complexes[i].index
            complexes[i] = complexes[i].convert_to_frames()
            complexes[i].index = complex_index

    @staticmethod
    def reset_transform(complex):
        # Must be used in conjuntion with `align_to`
        # to set the old_position and old_rotation values.
        if hasattr(complex, 'old_position'):
            complex.position = complex.old_position
        if hasattr(complex, 'old_rotation'):
            complex.rotation = complex.old_rotation

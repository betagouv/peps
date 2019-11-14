from .pepsenum import PepsEnum

class Problem(PepsEnum):
    DESHERBAGE = 1
    RAVAGEURS = 2
    DEPENSE = 3
    MALADIES_FONGIQUES = 4
    GLYPHOSATE = 6
    AUTRES = 5

    @property
    def display_text(self):
        display_texts = {
            'DESHERBAGE': 'Mieux gérer les adventices',
            'RAVAGEURS': 'Lutter contre les ravageurs',
            'DEPENSE': 'Réduire ma consommation des produits phytosanitaires',
            'MALADIES_FONGIQUES': 'Éviter des maladies fongiques',
            'GLYPHOSATE': 'Trouver des alternatives à l’utilisation du glyphosate',
            'AUTRES': 'Autres',
        }

        return display_texts.get(self.name) or self.name

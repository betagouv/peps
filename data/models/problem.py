from .pepsenum import PepsEnum

class Problem(PepsEnum):
    DESHERBAGE = 1
    RAVAGEURS = 2
    DEPENSE = 3
    MALADIES_FONGIQUES = 4
    AUTRES = 5

    @property
    def display_text(self):
        display_texts = {
            'DESHERBAGE': 'Mieux gérer les adventices',
            'RAVAGEURS': 'Lutter contre les ravageurs',
            'DEPENSE': 'Éviter des maladies fongiques',
            'MALADIES_FONGIQUES': 'Réduire ma consommation des produits phytosanitaires',
            'AUTRES': 'Autres',
        }

        return display_texts.get(self.name) or self.name

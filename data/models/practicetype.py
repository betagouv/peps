from .pepsenum import PepsEnum

class PracticeType(PepsEnum):
    REDUCTION_DOSES = 1
    ALLONGEMENT_ROTATION = 2
    NOUVELLES_CULTURES = 3
    TRAVAIL_DU_SOL = 4
    COUVERTS_VEGETAUX = 5
    FAUX_SEMIS = 6
    PLANTES_COMPAGNES = 7
    COUVERT_INTER_RANG = 8
    INSECTES_AUXILIAIRES = 9
    ALTERNER_PRINTEMPS_AUTOMNE = 10
    SEMIS_DIRECT = 11
    PLANTES_DE_SERVICE = 12

    @property
    def display_text(self):
        display_texts = {
            'REDUCTION_DOSES': 'Réduction des doses',
            'ALLONGEMENT_ROTATION': 'Allongement de la rotation',
            'NOUVELLES_CULTURES': 'Introduction des nouvelles cultures dans la rotation',
            'TRAVAIL_DU_SOL': 'Travail du sol',
            'COUVERTS_VEGETAUX': 'Couverts végétaux',
            'FAUX_SEMIS': 'Faux semis',
            'PLANTES_COMPAGNES': 'Plantes compagnes',
            'COUVERT_INTER_RANG': 'Couvert d\'inter-rang',
            'INSECTES_AUXILIAIRES': 'Insectes auxiliaires',
            'ALTERNER_PRINTEMPS_AUTOMNE': 'Alterner cultures de printemps et automne',
            'SEMIS_DIRECT': 'Semis direct',
            'PLANTES_DE_SERVICE': 'Plantes de service',
        }

        return display_texts.get(self.name) or self.name

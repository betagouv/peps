from .pepsenum import PepsEnum

class GlyphosateUses(PepsEnum):
    VIVACES = 1
    COUVERTS = 2
    PARCELLES = 3
    PRAIRIES = 4
    AUTRES = 5

    @property
    def display_text(self):
        display_texts = {
            'VIVACES': 'Gestion de vivaces',
            'COUVERTS': 'Destruction des couverts',
            'PARCELLES': 'Nettoyage des parcelles reverdies',
            'PRAIRIES': 'Destruction des prairies',
            'AUTRES': 'Autre',
        }

        return display_texts.get(self.name) or self.name

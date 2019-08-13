from .pepsenum import PepsEnum

class Pest(PepsEnum):
    MELIGETHES = 1
    CHARANCONS = 2
    PUCERONS = 3
    ALTISES = 4
    CECIDOMYIES = 5
    LIMACES = 6
    PYRALES = 7
    CICADELLES = 8
    DORYPHORES = 9
    AUTRES = 10
    SESAMIE = 11

    @property
    def display_text(self):
        display_texts = {
            'MELIGETHES': 'Méligèthes',
            'CHARANCONS': 'Charançons',
            'PUCERONS': 'Pucerons',
            'ALTISES': 'Altises',
            'CECIDOMYIES': 'Cécidomyies',
            'LIMACES': 'Limaces',
            'PYRALES': 'Pyrales',
            'CICADELLES': 'Cicadelles',
            'DORYPHORES': 'Doryphores',
            'AUTRES' :'Autres',
            'SESAMIE': 'Sésamie',
        }

        return display_texts.get(self.name) or self.name

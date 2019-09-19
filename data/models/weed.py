from .pepsenum import PepsEnum

class Weed(PepsEnum):
    RAY_GRASS = 1
    CHARDON = 2
    LISERON = 3
    VULPIN = 4
    RUMEX = 5
    LAITERON = 6
    AUTRES = 7
    GAILLET = 8
    GERANIUM = 9
    AMBROISE_ARMOISE = 10
    OROBRANCHE = 11

    @property
    def display_text(self):
        display_texts = {
            'RAY_GRASS': 'Ray-grass',
            'CHARDON': 'Chardon de champs',
            'LISERON': 'Liserons',
            'VULPIN': 'Vulpin de champs',
            'RUMEX': 'Rumex',
            'LAITERON': 'Laiteron de champs',
            'AUTRES': 'Autre',
            'GAILLET': 'Gaillet gratteron',
            'GERANIUM': 'Géranium',
            'AMBROISE_ARMOISE': 'Ambroisie à feuille d\'armoise',
            'OROBRANCHE': 'Orobanche',
        }

        return display_texts.get(self.name) or self.name

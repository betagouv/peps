from .pepsenum import PepsEnum


class Culture(PepsEnum):
    BLE = 1
    BLE_HIVER = 2
    BLE_PRINTEMPS = 3
    BETTRAVE = 4
    ORGE = 5
    MAIS = 6
    TOURNESOL = 7
    COLZA = 8
    AUTRES_CEREALES = 9
    AUTRES_LEGUMINEUSES = 10
    CHANVRE = 11
    AUTRES_OLEAGINEAUX = 12
    POIS = 13
    FEVEROLES = 14
    POMME_DE_TERRE = 15
    LIN = 16
    SOJA = 17
    PRAIRIES_CULTURES_FOURRAGERES = 18
    LENTILLES = 19
    SARRASIN = 20
    ORGE_PRINTEMPS = 21
    VIGNE = 22
    LUZERNE = 23

    @property
    def display_text(self):
        display_texts = {
            'BLE': 'Blé',
            'BLE_HIVER': 'Blé d\'hiver',
            'BLE_PRINTEMPS': 'Blé de printemps',
            'BETTRAVE': 'Bettrave',
            'ORGE': 'Orge',
            'MAIS': 'Maïs',
            'TOURNESOL': 'Tournesol',
            'COLZA': 'Colza',
            'AUTRES_CEREALES': 'Autres céreales',
            'AUTRES_LEGUMINEUSES': 'Autres légumineuses',
            'CHANVRE': 'Chanvre',
            'AUTRES_OLEAGINEAUX': 'Autres oléagineux',
            'POIS': 'Pois',
            'FEVEROLES': 'Féveroles',
            'POMME_DE_TERRE': 'Pomme de terre',
            'LIN': 'Lin',
            'SOJA': 'Soja',
            'PRAIRIES_CULTURES_FOURRAGERES': 'Prairies et cultures fourragères',
            'LENTILLES': 'Lentilles',
            'SARRASIN': 'Sarrasin',
            'ORGE_PRINTEMPS': 'Orge de printemps',
            'VIGNE': 'Vigne',
            'LUZERNE': 'Luzerne',
        }

        return display_texts.get(self.name) or self.name

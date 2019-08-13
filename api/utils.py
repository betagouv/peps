from django.utils.functional import cached_property
from data.models import Problem, Weed, Pest, Culture, PracticeType

class AlpacaUtils:

    answers = None

    def __init__(self, answers):
        self.answers = answers

    @cached_property
    def department(self):
        return self.answers.get('department')

    @cached_property
    def cultures(self):
        if not self.answers.get('rotation'):
            return None

        cultures_answers = self.answers['rotation']
        cultures = []

        for culture in cultures_answers:
            try:
                cultures.append(Culture[culture])
            except KeyError as _:
                continue

        return cultures

    @cached_property
    def soil_types(self):
        return None

    @cached_property
    def tillage_feasibility(self):
        return self.answers.get('tillage') == 'Oui'

    @cached_property
    def livestock(self):
        return self.answers.get('cattle') == 'Oui'

    @cached_property
    def direct_sale(self):
        return None

    @cached_property
    def advancement_level(self):
        advancement_level = self.answers.get('wheat')
        if not advancement_level:
            return None
        return float(advancement_level)

    @cached_property
    def problem(self):
        try:
            return Problem[self.answers.get('problem')]
        except KeyError as _:
            return None

    @cached_property
    def pests(self):
        return self._extract_enum_from_checkbox('pests', Pest)

    @cached_property
    def weeds(self):
        return self._extract_enum_from_checkbox('weeds', Weed)

    @cached_property
    def tested_practice_types(self):
        return self._extract_enum_from_checkbox('practices', PracticeType)

    def _extract_enum_from_checkbox(self, form_key, enum):
        form_value = self.answers.get(form_key)
        if not form_value:
            return None

        return_list = []
        for value in form_value.split(','):
            try:
                return_list.append(enum[value])
            except KeyError as _:
                continue
        return return_list

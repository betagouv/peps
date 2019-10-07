from django.utils.functional import cached_property
from django.core.exceptions import ValidationError
from data.models import Problem, PracticeTypeCategory, GlyphosateUses

class AlpacaUtils:

    answers = None

    def __init__(self, answers):
        self.answers = answers

    @cached_property
    def department(self):
        return self.answers.get('department')

    @cached_property
    def cultures(self):
        return self.answers.get('rotation')

    @cached_property
    def tillage_feasibility(self):
        return self.answers.get('tillage') == 'Oui'

    @cached_property
    def tillage(self):
        try:
            return PracticeTypeCategory[self.answers.get('tillage')]
        except KeyError as _:
            return None

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
        try:
            if self.answers.get('pests'):
                return self.answers.get('pests').split(',')
        except ValidationError as _:
            return None

    @cached_property
    def weeds(self):
        """
        This property will return either fields weeds, weedsGlyphosate, or perennials (all are treated
        the same by the engine and refer to weeds).
        """
        try:
            fields_with_weeds = ['weeds', 'perennials', 'weedsGlyphosate']
            for field in fields_with_weeds:
                if self.answers.get(field):
                    return self.answers.get(field).split(',')
        except ValidationError as _:
            return None

    @cached_property
    def glyphosate_uses(self):
        return self._extract_enum_from_checkbox('glyphosate', GlyphosateUses)

    @cached_property
    def tested_practice_types(self):
        return self._extract_enum_from_checkbox('practices', PracticeTypeCategory)

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

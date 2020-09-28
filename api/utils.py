import asana
from django.utils.functional import cached_property
from django.core.exceptions import ValidationError
from django.conf import settings
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
                answer = self.answers.get('pests')
                return answer if isinstance(answer, list) else answer.split(',')

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
                    answer = self.answers.get(field)
                    return answer if isinstance(answer, list) else answer.split(',')

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
        form_value = form_value if isinstance(form_value, list) else form_value.split(',')

        return_list = []
        for value in form_value:
            try:
                return_list.append(enum[value])
            except KeyError as _:
                continue
        return return_list


class AsanaUtils:
    """
    Utils to interact with Asana (e.g., task creation)
    """

    @staticmethod
    def send_task(projects, name, notes, due_at):
        client = asana.Client.access_token(settings.ASANA_PERSONAL_TOKEN)
        date = due_at.astimezone().isoformat() if due_at else None
        # pylint: disable=no-member
        client.tasks.create({
            'projects': projects,
            'due_at': date,
            'name': name,
            'notes': notes,
        })
        # pylint: enable=no-member

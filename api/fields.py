from rest_framework.fields import ChoiceField, empty
from rest_framework.utils import html
from django.utils.translation import gettext_lazy as _

class MultipleListChoiceField(ChoiceField):
    default_error_messages = {
        'invalid_choice': _('"{input}" is not a valid choice.'),
        'not_a_list': _('Expected a list of items but got type "{input_type}".'),
        'empty': _('This selection may not be empty.')
    }
    default_empty_html = []

    def __init__(self, *args, **kwargs):
        self.allow_empty = kwargs.pop('allow_empty', True)
        super().__init__(*args, **kwargs)

    def get_value(self, dictionary):
        if self.field_name not in dictionary:
            if getattr(self.root, 'partial', False):
                return empty
        # We override the default field access in order to support
        # lists in HTML forms.
        if html.is_html_input(dictionary):
            return dictionary.getlist(self.field_name)
        return dictionary.get(self.field_name, empty)

    def to_internal_value(self, data):
        if isinstance(data, str) or not hasattr(data, '__iter__'):
            self.fail('not_a_list', input_type=type(data).__name__)
        if not self.allow_empty and len(data) == 0:
            self.fail('empty')

        return list({
            super(MultipleListChoiceField, self).to_internal_value(item)
            for item in data
        })

    def to_representation(self, value):
        return list({
            self.choices.get(str(item), item) for item in value
        })

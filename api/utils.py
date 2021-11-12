import asana
from django.utils.functional import cached_property
from django.core.exceptions import ValidationError
from django.conf import settings

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

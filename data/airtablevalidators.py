from data.models import Problem

class AirtableError():
    def __init__(self, message, fatal=True, url=None):
        self.message = message
        self.fatal = fatal
        self.url = url
    def __str__(self):
        return '%s --- (%s)' % (self.message, self.url)
    __repr__ = __str__

def validate_practices(airtable_practices):
    """
    Returns an array of errors from airtable practices
    """
    errors = []

    def get_practice_errors(practice):
        errors = []
        fields = practice['fields']
        practice_id = practice['id']
        practice_title = fields.get('Nom')
        url = 'https://airtable.com/tblobpdQDxkzcllWo/viwIl6ySkIGCg2zPW/%s' % practice_id

        if not practice_title:
            message = 'Pratique ID %s n\'a pas de titre (colonne Nom)' % practice_id
            errors.append(AirtableError(message, url=url))

        if not fields.get('Description'):
            message = 'Pratique "%s" (ID %s) manque la description (colonne Description)' % (practice_title, practice_id)
            errors.append(AirtableError(message, url=url))

        if not fields.get('CTA lien'):
            message = 'Pratique "%s" (ID %s) n\'a pas de lien CTA (colonne CTA lien)' % (practice_title, practice_id)
            errors.append(AirtableError(message, url=url))

        if len(fields.get('CTA lien', [])) > 1:
            message = 'Pratique "%s" (ID %s) a plusieurs liens CTA, il faut en avoir un seul (colonne CTA lien)' % (practice_title, practice_id)
            errors.append(AirtableError(message, url=url))

        if not fields.get('CTA title'):
            message = 'Pratique "%s" (ID %s) n\'a pas de titre CTA (colonne CTA title)' % (practice_title, practice_id)
            errors.append(AirtableError(message, url=url))

        if not fields.get('Types'):
            message = 'Pratique "%s" (ID %s) n\'a pas de type (colonne Types)' % (practice_title, practice_id)
            errors.append(AirtableError(message, fatal=False, url=url))

        for json_problem in fields.get('Problèmes adressés', []):
            try:
                Problem[json_problem]
            except KeyError as _:
                message = 'Pratique "%s" (ID %s) a un problème pas connu (%s, colonne Problèmes adressés)' % (practice_title, practice_id, json_problem)
                errors.append(AirtableError(message, fatal=False, url=url))

        if not fields.get('Marges de manoeuvre'):
            message = 'Pratique "%s" (ID %s) n\'a pas de marges de manoeuvre (colonne Marges de manoeuvre)' % (practice_title, practice_id)
            errors.append(AirtableError(message, fatal=False, url=url))

        if not fields.get('Liens'):
            message = 'Pratique "%s" (ID %s) n\'a pas de liens (colonne Liens)' % (practice_title, practice_id)
            errors.append(AirtableError(message, fatal=False, url=url))

        if fields.get('Matériel') and fields.get('Matériel')[0].islower():
            message = 'Le matériel de la pratique "%s" (ID %s) commence par une lettre en minuscule' % (practice_title, practice_id)
            errors.append(AirtableError(message, fatal=False, url=url))

        if fields.get('Période de travail') and fields.get('Période de travail')[0].islower():
            message = 'La période de travail de la pratique "%s" (ID %s) commence par une lettre en minuscule' % (practice_title, practice_id)
            errors.append(AirtableError(message, fatal=False, url=url))

        if fields.get('Nom') and fields.get('Nom')[0].islower():
            message = 'La nom/titre de la pratique "%s" (ID %s) commence par une lettre en minuscule' % (practice_title, practice_id)
            errors.append(AirtableError(message, fatal=False, url=url))

        if fields.get('Impact') and fields.get('Impact')[0].islower():
            message = 'L\'impact de la pratique "%s" (ID %s) commence par une lettre en minuscule' % (practice_title, practice_id)
            errors.append(AirtableError(message, fatal=False, url=url))

        return errors

    for practice in airtable_practices:
        errors += get_practice_errors(practice)

    return errors

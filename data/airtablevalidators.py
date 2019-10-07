from data.models import Problem, PracticeTypeCategory, GlyphosateUses

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

        if not fields.get('Difficulté'):
            message = 'Pratique "%s" (ID %s) n\'a pas de difficulté (colonne Difficulté)' % (practice_title, practice_id)
            errors.append(AirtableError(message, url=url))

        if fields.get('Difficulté') and (fields.get('Difficulté') > 1 or fields.get('Difficulté') < 0):
            message = 'Pratique "%s" (ID %s) a une difficulté incorrecte (ça doit être entre 0 et 1)' % (practice_title, practice_id)
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

        if fields.get('Matériel') and fields.get('Matériel')[0].islower():
            message = 'Le matériel de la pratique "%s" (ID %s) commence par une lettre en minuscule (colonne Matériel)' % (practice_title, practice_id)
            errors.append(AirtableError(message, fatal=False, url=url))

        if fields.get('Période de travail') and fields.get('Période de travail')[0].islower():
            message = 'La période de travail de la pratique "%s" (ID %s) commence par une lettre en minuscule (colonne Période de travail)' % (practice_title, practice_id)
            errors.append(AirtableError(message, fatal=False, url=url))

        if fields.get('Nom') and fields.get('Nom')[0].islower():
            message = 'La nom/titre de la pratique "%s" (ID %s) commence par une lettre en minuscule (colonne Nom)' % (practice_title, practice_id)
            errors.append(AirtableError(message, fatal=False, url=url))

        if fields.get('Impact') and fields.get('Impact')[0].islower():
            message = 'L\'impact de la pratique "%s" (ID %s) commence par une lettre en minuscule (colonne Impact)' % (practice_title, practice_id)
            errors.append(AirtableError(message, fatal=False, url=url))

        if fields.get('Bénéfices supplémentaires') and fields.get('Bénéfices supplémentaires')[0].islower():
            message = 'Les bénéfices supplémentaires de la pratique "%s" (ID %s) commence par une lettre en minuscule (colonne Bénéfices supplémentaires)' % (practice_title, practice_id)
            errors.append(AirtableError(message, fatal=False, url=url))

        if fields.get('Facteur clé de succès') and fields.get('Facteur clé de succès')[0].islower():
            message = 'Le facteur clé de succès de la pratique "%s" (ID %s) commence par une lettre en minuscule (colonne Facteur clé de succès)' % (practice_title, practice_id)
            errors.append(AirtableError(message, fatal=False, url=url))

        if fields.get('Description') and fields.get('Description')[0].islower():
            message = 'La description de la pratique "%s" (ID %s) commence par une lettre en minuscule (colonne Description)' % (practice_title, practice_id)
            errors.append(AirtableError(message, fatal=False, url=url))

        if fields.get('CTA title') and fields.get('CTA title')[0].islower():
            message = 'Le label CTA de la pratique "%s" (ID %s) commence par une lettre en minuscule (colonne CTA title)' % (practice_title, practice_id)
            errors.append(AirtableError(message, fatal=False, url=url))

        return errors

    for practice in airtable_practices:
        errors += get_practice_errors(practice)

    return errors


def validate_practice_types(airtable_practice_types):
    """
    Returns an array of errors from airtable practice types
    """
    errors = []

    def get_practice_type_errors(practice_type):
        errors = []
        fields = practice_type['fields']
        practice_type_id = practice_type['id']
        practice_type_title = fields.get('Name')
        url = 'https://airtable.com/tblTwpbVXTqbQAYfB/viw3CI0bd8IFbmjAn/%s' % practice_type_id

        if not practice_type_title:
            message = 'Type de pratique ID %s n\'a pas de nom (colonne Name)' % practice_type_id
            errors.append(AirtableError(message, url=url))

        if not fields.get('Enum code'):
            message = 'Type de pratique "%s" (ID %s) manque l\'enum code (colonne Enum code)' % (practice_type_title, practice_type_id)
            errors.append(AirtableError(message, url=url))

        if fields.get('Malus') and (fields.get('Malus') < 0 or fields.get('Malus') > 1):
            message = 'Type de pratique "%s" (ID %s) a un malus invalide (ça doit être entre 0 et 1)' % (practice_type_title, practice_type_id)
            errors.append(AirtableError(message, url=url))

        if fields.get('Enum code'):
            try:
                PracticeTypeCategory[fields.get('Enum code')]
            except KeyError as _:
                message = 'Type de pratique "%s" (ID %s) a un code enum qui n\'est pas connu du backend' % (practice_type_title, practice_type_id)
                errors.append(AirtableError(message, url=url))

        return errors

    for practice_type in airtable_practice_types:
        errors += get_practice_type_errors(practice_type)

    return errors


def validate_weeds(airtable_weeds):
    """
    Returns an array of errors from airtable weeds
    """
    errors = []

    def get_weed_errors(weed):
        errors = []
        fields = weed['fields']
        weed_id = weed['id']
        weed_title = fields.get('Name')
        url = 'https://airtable.com/tblP1PaSoX4gV7p1b/viw8IcVom4xuyy07U/%s' % weed_id

        if not weed_title:
            message = 'Adventice ID %s n\'a pas de nom (colonne Name)' % weed_id
            errors.append(AirtableError(message, url=url))

        return errors

    for weed in airtable_weeds:
        errors += get_weed_errors(weed)

    return errors


def validate_pests(airtable_pests):
    """
    Returns an array of errors from airtable pests
    """
    errors = []

    def get_pest_errors(pest):
        errors = []
        fields = pest['fields']
        pest_id = pest['id']
        pest_title = fields.get('Name')
        url = 'https://airtable.com/tblhYO3O0Dfb3mPvj/viwKKEA7J64iS0UPS/%s' % pest_id

        if not pest_title:
            message = 'Ravageur ID %s n\'a pas de nom (colonne Name)' % pest_id
            errors.append(AirtableError(message, url=url))

        return errors

    for pest in airtable_pests:
        errors += get_pest_errors(pest)

    return errors


def validate_cultures(airtable_cultures):
    """
    Returns an array of errors from airtable cultures
    """
    errors = []

    def get_culture_errors(culture):
        errors = []
        fields = culture['fields']
        culture_id = culture['id']
        culture_title = fields.get('Name')
        url = 'https://airtable.com/tblbHAN04NniLVT5d/viw4vPP8z0awDZaBG/%s' % culture_id

        if not culture_title:
            message = 'Culture ID %s n\'a pas de nom (colonne Name)' % culture_id
            errors.append(AirtableError(message, url=url))

        return errors

    for pest in airtable_cultures:
        errors += get_culture_errors(pest)

    return errors


def validate_glyphosate_uses(airtable_glyphosate):
    """
    Returns an array of errors from airtable glyphosate uses
    """
    errors = []

    def get_glyphosate_errors(glyphosate):
        errors = []
        fields = glyphosate['fields']
        glyphosate_id = glyphosate['id']
        glyphosate_title = fields.get('Name')
        url = 'https://airtable.com/tbll1HAaLtuUqwFOy/viwtrkk3q5twjupNn/recoU540M3R2rEN8U/%s' % glyphosate_id

        if not glyphosate_title:
            message = 'L\'usage de glyphosate ID %s n\'a pas de nom (colonne Name)' % glyphosate_id
            errors.append(AirtableError(message, url=url))

        if not fields.get('Enum code'):
            message = 'L\'usage de glyphosate "%s" (ID %s) manque l\'enum code (colonne Enum code)' % (glyphosate_title, glyphosate_id)
            errors.append(AirtableError(message, url=url))

        if fields.get('Enum code'):
            try:
                GlyphosateUses[fields.get('Enum code')]
            except KeyError as _:
                message = 'L\'usage de glyphosate "%s" (ID %s) a un code enum qui n\'est pas connu du backend' % (glyphosate_title, glyphosate_id)
                errors.append(AirtableError(message, fatal=False, url=url))

        return errors

    for pest in airtable_glyphosate:
        errors += get_glyphosate_errors(pest)

    return errors


def validate_resources(airtable_resources):
    """
    Returns an array of errors from airtable resources
    """
    errors = []

    def get_resource_errors(resource):
        errors = []
        fields = resource['fields']
        resource_id = resource['id']
        resource_title = fields.get('Nom')
        url = 'https://airtable.com/tblVb2GDuCPGUrt35/viwRtOVqMHzJtgvNn/%s' % resource_id

        if not resource_title:
            message = 'Lien ID %s n\'a pas de nom (colonne Nom)' % resource_id
            errors.append(AirtableError(message, url=url))

        if not fields.get('Url'):
            message = 'Lien "%s" (ID %s) manque l\'URL (colonne Url)' % (resource_title, resource_id)
            errors.append(AirtableError(message, url=url))

        if not fields.get('Type'):
            message = 'Lien "%s" (ID %s) manque le type (colonne Type)' % (resource_title, resource_id)
            errors.append(AirtableError(message, url=url))

        if not fields.get('Description'):
            message = 'Lien "%s" (ID %s) manque la description (colonne Description)' % (resource_title, resource_id)
            errors.append(AirtableError(message, fatal=False, url=url))

        return errors

    for pest in airtable_resources:
        errors += get_resource_errors(pest)

    return errors

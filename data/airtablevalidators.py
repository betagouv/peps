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

        if not fields.get('Nom court'):
            message = 'Pratique "%s" (ID %s) manque le nom court (colonne Nom court)' % (practice_title, practice_id)
            errors.append(AirtableError(message, url=url))

        if not fields.get('Description'):
            message = 'Pratique "%s" (ID %s) manque la description (colonne Description)' % (practice_title, practice_id)
            errors.append(AirtableError(message, url=url))

        if not fields.get('Types'):
            message = 'Pratique "%s" (ID %s) n\'a pas de type (colonne Types)' % (practice_title, practice_id)
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

        if fields.get('Image principale') and fields.get('Image principale')[0].get('size') > 400000:
            size = fields.get('Image principale')[0].get('size') / 1000
            message = 'Pratique "%s" (ID %s) a une image trop lourde (ça pèse %s ko)' % (practice_title, practice_id, str(size))
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

        if not fields.get('Matériel') and not fields.get('Période de travail') and not fields.get('Impact') and not fields.get('Bénéfices supplémentaires') and not fields.get('Facteur clé de succès'):
            message = 'La pratique "%s" (ID %s) n\'a aucune information additionelle. Il faut au moins une parmi : matériel, période de travail, impact, bénéfices supplémentaires, ou facteur clé de succès' % (practice_title, practice_id)
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

    for culture in airtable_cultures:
        errors += get_culture_errors(culture)

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

    for usage in airtable_glyphosate:
        errors += get_glyphosate_errors(usage)

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
        resource_url = fields.get('Url')
        url = 'https://airtable.com/tblVb2GDuCPGUrt35/viwRtOVqMHzJtgvNn/%s' % resource_id

        if not resource_title:
            message = 'Lien ID %s n\'a pas de nom (colonne Nom)' % resource_id
            errors.append(AirtableError(message, url=url))

        if not resource_url:
            message = 'Lien "%s" (ID %s) manque l\'URL (colonne Url)' % (resource_title, resource_id)
            errors.append(AirtableError(message, url=url))

        if not fields.get('Type'):
            message = 'Lien "%s" (ID %s) manque le type (colonne Type)' % (resource_title, resource_id)
            errors.append(AirtableError(message, url=url))

        if not fields.get('Description'):
            message = 'Lien "%s" (ID %s) manque la description (colonne Description)' % (resource_title, resource_id)
            errors.append(AirtableError(message, fatal=False, url=url))

        if resource_url and 'youtube' in resource_url and ('?t=' in resource_url or '&t=' in resource_url):
            message = 'Lien Youtube "%s" (ID %s) contient le temps de démarrage dans l\'url' % (resource_title, resource_id)
            errors.append(AirtableError(message, fatal=False, url=url))

        return errors

    for resource in airtable_resources:
        errors += get_resource_errors(resource)

    return errors


def validate_categories(airtable_categories):
    """
    Returns an array of errors from categories
    """
    errors = []

    def get_category_errors(category):
        errors = []
        fields = category['fields']
        category_id = category['id']
        category_title = fields.get('Title')
        category_image = fields.get('Image')
        url = 'https://airtable.com/tblJ8W5fjnatj4hki/%s' % category_id

        if not category_title:
            message = 'La categorie ID %s n\'a pas de title (colonne Title)' % category_id
            errors.append(AirtableError(message, url=url))

        if not category_image:
            message = 'La categorie "%s" (ID %s) n\'a pas d\'image (colonne Image)' % (category_title, category_id)
            errors.append(AirtableError(message, url=url))

        if not fields.get('Practices'):
            message = 'La categorie "%s" (ID %s) n\'a pas de pratiques assignées (colonne Practices)' % (category_title, category_id)
            errors.append(AirtableError(message, url=url))

        if not fields.get('Description'):
            message = 'La categorie "%s" (ID %s) n\'a pas de description (colonne Description)' % (category_title, category_id)
            errors.append(AirtableError(message, fatal=False, url=url))

        return errors

    for category in airtable_categories:
        errors += get_category_errors(category)

    return errors


def validate_weed_practices(airtable_weed_practices):
    """
    Returns an array of errors from weed_practices
    """
    errors = []

    def get_weed_practice_errors(weed_practice):
        errors = []
        fields = weed_practice['fields']
        weed_practice_id = weed_practice['id']
        url = 'https://airtable.com/tbl0RJ5WcrI0SsxvZ/%s' % weed_practice_id

        if not fields.get('Adventice'):
            message = 'La relation adventice-pratique ID %s n\'a pas d\'adventice (colonne Adventice)' % weed_practice_id
            errors.append(AirtableError(message, url=url))

        if not fields.get('Pratique'):
            message = 'La relation adventice-pratique ID %s n\'a pas de pratique (colonne Pratique)' % weed_practice_id
            errors.append(AirtableError(message, url=url))

        if fields.get('Multiplicateur') != 0 and not fields.get('Multiplicateur'):
            message = 'La relation adventice-pratique ID %s n\'a pas de multiplicateur (colonne Multiplicateur)' % weed_practice_id
            errors.append(AirtableError(message, url=url))

        return errors

    for weed_practice in airtable_weed_practices:
        errors += get_weed_practice_errors(weed_practice)

    return errors


def validate_pest_practices(airtable_pest_practices):
    """
    Returns an array of errors from pest_practices
    """
    errors = []

    def get_pest_practice_errors(pest_practice):
        errors = []
        fields = pest_practice['fields']
        pest_practice_id = pest_practice['id']
        url = 'https://airtable.com/tblt8SSfxOGH8XEQC/%s' % pest_practice_id

        if not fields.get('Ravageur'):
            message = 'La relation ravageur-pratique ID %s n\'a pas de ravageur (colonne Ravageur)' % pest_practice_id
            errors.append(AirtableError(message, url=url))

        if not fields.get('Pratique'):
            message = 'La relation ravageur-pratique ID %s n\'a pas de pratique (colonne Pratique)' % pest_practice_id
            errors.append(AirtableError(message, url=url))

        if fields.get('Multiplicateur') != 0 and not fields.get('Multiplicateur'):
            message = 'La relation ravageur-pratique ID %s n\'a pas de multiplicateur (colonne Multiplicateur)' % pest_practice_id
            errors.append(AirtableError(message, url=url))

        return errors

    for pest_practice in airtable_pest_practices:
        errors += get_pest_practice_errors(pest_practice)

    return errors


def validate_culture_practices(airtable_culture_practices):
    """
    Returns an array of errors from culture_practices
    """
    errors = []

    def get_culture_practice_errors(culture_practice):
        errors = []
        fields = culture_practice['fields']
        culture_practice_id = culture_practice['id']
        url = 'https://airtable.com/tblw6bJT2yuubwVcD/%s' % culture_practice_id

        if not fields.get('Culture'):
            message = 'La relation culture-pratique ID %s n\'a pas de culture (colonne Culture)' % culture_practice_id
            errors.append(AirtableError(message, url=url))

        if not fields.get('Pratique'):
            message = 'La relation culture-pratique ID %s n\'a pas de pratique (colonne Pratique)' % culture_practice_id
            errors.append(AirtableError(message, url=url))

        if fields.get('Multiplicateur') != 0 and not fields.get('Multiplicateur'):
            message = 'La relation culture-pratique ID %s n\'a pas de multiplicateur (colonne Multiplicateur)' % culture_practice_id
            errors.append(AirtableError(message, url=url))

        return errors

    for culture_practice in airtable_culture_practices:
        errors += get_culture_practice_errors(culture_practice)

    return errors


def validate_department_practices(airtable_department_practices):
    """
    Returns an array of errors from department_practices
    """
    errors = []

    def get_department_practice_errors(department_practice):
        errors = []
        fields = department_practice['fields']
        department_practice_id = department_practice['id']
        url = 'https://airtable.com/tblvPvX53ywyv4hSd/%s' % department_practice_id

        if not fields.get('Departement'):
            message = 'La relation departement-pratique ID %s n\'a pas de departement (colonne Departement)' % department_practice_id
            errors.append(AirtableError(message, url=url))

        if not fields.get('Pratique'):
            message = 'La relation departement-pratique ID %s n\'a pas de pratique (colonne Pratique)' % department_practice_id
            errors.append(AirtableError(message, url=url))

        if fields.get('Multiplicateur') != 0 and not fields.get('Multiplicateur'):
            message = 'La relation departement-pratique ID %s n\'a pas de multiplicateur (colonne Multiplicateur)' % department_practice_id
            errors.append(AirtableError(message, url=url))

        return errors

    for department_practice in airtable_department_practices:
        errors += get_department_practice_errors(department_practice)

    return errors


def validate_glyphosate_practices(airtable_glyphosate_practices):
    """
    Returns an array of errors from glyphosate_practices
    """
    errors = []

    def get_glyphosate_practice_errors(glyphosate_practice):
        errors = []
        fields = glyphosate_practice['fields']
        glyphosate_practice_id = glyphosate_practice['id']
        url = 'https://airtable.com/tblOOxxMTQS785Vmd/%s' % glyphosate_practice_id

        if not fields.get('Glyphosate'):
            message = 'La relation glyphosate-pratique ID %s n\'a pas de glyphosate (colonne Glyphosate)' % glyphosate_practice_id
            errors.append(AirtableError(message, url=url))

        if not fields.get('Pratique'):
            message = 'La relation glyphosate-pratique ID %s n\'a pas de pratique (colonne Pratique)' % glyphosate_practice_id
            errors.append(AirtableError(message, url=url))

        if fields.get('Multiplicateur') != 0 and not fields.get('Multiplicateur'):
            message = 'La relation glyphosate-pratique ID %s n\'a pas de multiplicateur (colonne Multiplicateur)' % glyphosate_practice_id
            errors.append(AirtableError(message, url=url))

        return errors

    for glyphosate_practice in airtable_glyphosate_practices:
        errors += get_glyphosate_practice_errors(glyphosate_practice)

    return errors


def validate_departments(airtable_departments):
    """
    Returns an array of errors from department objects
    """
    errors = []

    def get_department_errors(department):
        errors = []
        fields = department['fields']
        department_id = department['id']
        url = 'https://airtable.com/tblIlOOrHgCPGBKpI/%s' % department_id

        if not fields.get('Numéro'):
            message = 'Le departement ID %s n\'a pas de numéro (colonne Numéro)' % department_id
            errors.append(AirtableError(message, url=url))

        if not fields.get('Nom'):
            message = 'Le departement ID %s n\'a pas de nom (colonne Nom)' % department_id
            errors.append(AirtableError(message, url=url))

        return errors

    for department in airtable_departments:
        errors += get_department_errors(department)

    return errors


def validate_practice_groups(airtable_practice_groups):
    """
    Returns an array of errors from practice group objects
    """
    errors = []

    def get_practice_group_errors(practice_group):
        errors = []
        fields = practice_group['fields']
        name = fields.get('Nom')
        practice_group_id = practice_group['id']
        url = 'https://airtable.com/tblN8TqSSncgOJewG/%s' % practice_group_id

        if not name:
            message = 'La famille ID %s n\'a pas de nom (colonne Nom)' % practice_group_id
            errors.append(AirtableError(message, url=url))

        if not fields.get('Pratiques'):
            message = 'La famille %s (ID %s) n\'a pas de pratiques (colonne Pratiques)' % (name, practice_group_id)
            errors.append(AirtableError(message, fatal=False, url=url))

        if not fields.get('Description'):
            message = 'La famille %s (ID %s) n\'a pas de description (colonne Description)' % (name, practice_group_id)
            errors.append(AirtableError(message, fatal=False, url=url))

        return errors

    for practice_group in airtable_practice_groups:
        errors += get_practice_group_errors(practice_group)

    return errors


def validate_mechanisms(airtable_mechanisms):
    """
    Returns an array of errors from mechanism objects
    """
    errors = []

    def get_mechanism_errors(mechanism):
        errors = []
        fields = mechanism['fields']
        name = fields.get('Name')
        mechanism_id = mechanism['id']
        url = 'https://airtable.com/tbliz8fD7ZaoqIugz/%s' % mechanism_id

        if not name:
            message = 'La marge de manoeuvre ID %s n\'a pas de nom (colonne Name)' % mechanism_id
            errors.append(AirtableError(message, url=url))

        if not fields.get('Description'):
            message = 'La marge de manoeuvre %s (ID %s) n\'a pas de description (colonne Description)' % (name, mechanism_id)
            errors.append(AirtableError(message, fatal=False, url=url))

        if not fields.get('Pratiques'):
            message = 'La marge de manoeuvre %s (ID %s) n\'a pas de pratiques (colonne Pratiques)' % (name, mechanism_id)
            errors.append(AirtableError(message, fatal=False, url=url))

        return errors

    for mechanism in airtable_mechanisms:
        errors += get_mechanism_errors(mechanism)

    return errors

def validate_resource_images(airtable_resource_images):
    """
    Returns an array of errors from resource-images objects
    """
    errors = []

    def get_resource_image_errors(resource_images):
        errors = []
        fields = resource_images['fields']
        structure = fields.get('Structure')
        url = fields.get('URL_principal')
        resource_image_id = resource_images['id']
        airtable_url = 'https://airtable.com/tbltygkXhxF6bBKXY/%s' % resource_image_id

        if not structure:
            message = 'Le logo ID %s n\'a pas de structure (colonne Structure)' % resource_image_id
            errors.append(AirtableError(message, url=airtable_url))

        if not url:
            message = 'Le logo %s (ID %s) n\'a pas d\'URL (colonne URL_principal)' % (structure, resource_image_id)
            errors.append(AirtableError(message, url=airtable_url))

        if not fields.get('logo'):
            message = 'Le logo %s (ID %s) n\'a pas d\'image (colonne logo)' % (structure, resource_image_id)
            errors.append(AirtableError(message, url=airtable_url))

        return errors

    for resource_images in airtable_resource_images:
        errors += get_resource_image_errors(resource_images)

    return errors

def validate_farmers(airtable_farmers):
    """
    Returns an array of errors from farmer objects
    """
    errors = []

    def get_farmer_errors(farmer):
        errors = []
        fields = farmer['fields']
        name = fields.get('Prénom et Nom')
        farmer_id = farmer['id']
        airtable_url = 'https://airtable.com/tblwbHvoVKo0o9C38/%s' % farmer_id

        if not name:
            message = 'L\'agriculteur %s n\'a pas de nom/prénon (colonne Prénom et Nom)' % farmer_id
            errors.append(AirtableError(message, url=airtable_url))

        if not fields.get('Latitude') or not fields.get('Longitude'):
            message = 'L\'agriculteur %s (ID %s) n\'a pas des données de geoloc (colonnes Latitude et Longitude)' % (name, farmer_id)
            errors.append(AirtableError(message, url=airtable_url))

        return errors

    for farmer in airtable_farmers:
        errors += get_farmer_errors(farmer)

    return errors

def validate_experiments(airtable_experiments):
    """
    Returns an array of errors from experiment objects
    """
    errors = []

    def get_experiment_errors(experiment):
        errors = []
        fields = experiment['fields']
        name = fields.get('Titre de l\'XP')
        experiment_id = experiment['id']
        airtable_url = 'https://airtable.com/tbl7jwg9D5NhH8LSH/%s' % experiment_id

        if not name:
            message = 'L\'exploitation %s n\'a pas de titre (colonne Titre de l\'XP)' % experiment_id
            errors.append(AirtableError(message, url=airtable_url))

        if not fields.get('Agriculteur'):
            message = 'L\'exploitation %s (ID %s) n\'est pas liée à un agriculteur (colonne Agriculteur)' % (name, experiment_id)
            errors.append(AirtableError(message, url=airtable_url))

        return errors

    for experiment in airtable_experiments:
        errors += get_experiment_errors(experiment)

    return errors

import time
import json
import requests
from django.conf import settings
from django.utils import timezone
from data.models import Problem, PracticeType, Weed, Pest, Resource, ResourceType, GlyphosateUses
from data.models import Culture, Practice, PracticeGroup, Mechanism, PracticeTypeCategory
from data.airtablevalidators import validate_practices, validate_practice_types, validate_weeds
from data.airtablevalidators import validate_pests, validate_cultures, validate_glyphosate_uses


class AirtableAdapter:
    """
    Updates the existing models from Airtable records.
    """

    @staticmethod
    def update_practices():
        """
        We completely replace whatever we have in the DB for
        the new information. Eventually we may want to only replace
        the changed ones.

        If there are errors, an array of them will be returned.
        """
        errors = []

        # Fetch Airtable data and validate it if needed
        json_practices = _get_airtable_data('Pratiques?view=Grid%20view')
        errors += validate_practices(json_practices)

        json_practice_types = _get_airtable_data('Types%20de%20pratique?view=Grid%20view')
        errors += validate_practice_types(json_practice_types)

        json_weeds = _get_airtable_data('Adventices?view=Grid%20view')
        errors += validate_weeds(json_weeds)

        json_pests = _get_airtable_data('Ravageurs?view=Grid%20view')
        errors += validate_pests(json_pests)

        json_cultures = _get_airtable_data('Cultures?view=Grid%20view')
        errors += validate_cultures(json_cultures)

        json_glyphosate = _get_airtable_data('Glyphosate?view=Grid%20view')
        errors += validate_glyphosate_uses(json_glyphosate)

        json_culture_practices = _get_airtable_data('Pratiques%2FCultures?view=Grid%20view')
        json_departments_practices = _get_airtable_data('Pratiques%2FDepartements?view=Grid%20view')
        json_departments = _get_airtable_data('Departements?view=Grid%20view')
        json_weed_practices = _get_airtable_data('Pratiques%2FAdventices?view=Grid%20view')
        json_pest_practices = _get_airtable_data('Pratiques%2FRavageurs?view=Grid%20view')
        json_glyphosate_practices = _get_airtable_data('Pratiques%2FGlyphosate?view=Grid%20view')
        json_practice_groups = _get_airtable_data('Familles?view=Grid%20view')
        json_mechanisms = _get_airtable_data('Marges%20de%20manoeuvre?view=Grid%20view')
        json_resources = _get_airtable_data('Liens?view=Grid%20view')

        has_fatal_errors = any(x.fatal for x in errors)
        if has_fatal_errors:
            return errors

        mechanisms = _fetch_mechanisms(json_mechanisms)

        Mechanism.objects.all().delete()
        for mechanism in mechanisms:
            mechanism.save()

        resources = _fetch_resources(json_resources)
        Resource.objects.all().delete()
        for resource in resources:
            resource.save()

        practices = _fetch_practices(json_practices, json_cultures, json_culture_practices, json_departments_practices,
                                     json_departments, json_weeds, json_weed_practices, json_pests, json_pest_practices, json_glyphosate,
                                     json_glyphosate_practices, mechanisms, resources)
        practice_groups = _fetch_pratice_groups(json_practice_groups)
        practice_types = _fetch_practice_types(json_practice_types)

        PracticeGroup.objects.all().delete()
        for practice_group in practice_groups:
            practice_group.save()

        PracticeType.objects.all().delete()
        for practice_type in practice_types:
            practice_type.save()

        Practice.objects.all().delete()
        for practice in practices:
            practice.save()

        _link_practices_with_groups(practices, practice_groups)
        _link_practices_with_resources(practices, resources)
        _link_practices_with_types(practices, practice_types)

        return errors


def _fetch_practices(json_practices, json_cultures, json_culture_practices, json_departments_practices,
                     json_departments, json_weeds, json_weed_practices, json_pests, json_pest_practices, json_glyphosate,
                     json_glyphosate_practices, mechanisms, resources):
    practices = []
    for json_practice in json_practices:
        practices.append(Practice(
            external_id=json_practice.get('id'),
            mechanism=_get_mechanism(json_practice, mechanisms),
            main_resource=_get_main_resource(json_practice, resources),
            main_resource_label=json_practice['fields'].get('CTA title'),
            airtable_json=json_practice,
            airtable_url='https://airtable.com/tblobpdQDxkzcllWo/' + json_practice.get('id') + '/',
            title=json_practice['fields'].get('Nom'),
            description=json_practice['fields'].get('Description'),
            equipment=json_practice['fields'].get('Matériel'),
            schedule=json_practice['fields'].get('Période de travail'),
            impact=json_practice['fields'].get('Impact'),
            additional_benefits=json_practice['fields'].get('Bénéfices supplémentaires'),
            success_factors=json_practice['fields'].get('Facteur clé de succès'),
            needs_tillage=json_practice['fields'].get('Nécessite travail du sol', False),
            livestock_multiplier=json_practice['fields'].get('Élevage multiplicateur'),
            needs_livestock=json_practice['fields'].get('Élevage nécessaire', False),
            direct_sale_multiplier=json_practice['fields'].get('Vente directe multiplicateur'),
            precision=json_practice['fields'].get('Précision'),
            difficulty=json_practice['fields'].get('Difficulté'),
            added_cultures=_get_added_cultures(json_practice, json_cultures),
            culture_whitelist=_get_culture_whitelist(json_practice, json_cultures),
            weed_whitelist=_get_weeds(json_practice, json_weeds),
            pest_whitelist=_get_pests(json_practice, json_pests),
            problems_addressed=_get_problems_addressed(json_practice),
            image_url=_get_image_url(json_practice),
            department_multipliers=_get_department_multipliers(json_practice, json_departments_practices, json_departments),
            weed_multipliers=_get_weed_multipliers(json_practice, json_weeds, json_weed_practices),
            pest_multipliers=_get_pest_multipliers(json_practice, json_pests, json_pest_practices),
            glyphosate_multipliers=_get_glyphosate_multipliers(json_practice, json_glyphosate, json_glyphosate_practices),
            culture_multipliers=_get_culture_multipliers(json_practice, json_cultures, json_culture_practices),
            modification_date=timezone.now(),
        ))

    return practices


def _fetch_pratice_groups(json_practice_groups):

    practice_groups = []
    for json_practice_group in json_practice_groups:
        practice_groups.append(PracticeGroup(
            external_id=json_practice_group.get('id'),
            airtable_json=json_practice_group,
            modification_date=timezone.now(),
            name=json_practice_group['fields'].get('Nom'),
            description=json_practice_group['fields'].get('Description'),
        ))
    return practice_groups


def _fetch_practice_types(json_practice_types):

    practice_types = []
    for json_practice_type in json_practice_types:
        practice_types.append(PracticeType(
            external_id=json_practice_type.get('id'),
            airtable_json=json_practice_type,
            airtable_url='https://airtable.com/tblTwpbVXTqbQAYfB/' + json_practice_type.get('id') + '/',
            modification_date=timezone.now(),
            display_text=json_practice_type['fields'].get('Name'),
            penalty=json_practice_type['fields'].get('Malus'),
            category=_get_practice_type_category(json_practice_type),
        ))
    return practice_types

def _get_practice_type_category(json_practice_type):
    try:
        return PracticeTypeCategory[json_practice_type['fields'].get('Enum code')].value
    except Exception as _:
        return None

def _link_practices_with_groups(practices, practice_groups):
    for practice in practices:
        if practice.airtable_json:
            groups = practice.airtable_json['fields'].get('Familles', [])
            practice.practice_groups.set(list(x for x in practice_groups if x.external_id in groups))


def _link_practices_with_resources(practices, resources):
    for practice in practices:
        if practice.airtable_json:
            secondary_resource_ids = practice.airtable_json['fields'].get('Liens', [])
            practice.secondary_resources.set(list(x for x in resources if x.external_id in secondary_resource_ids))

def _link_practices_with_types(practices, types):
    for practice in practices:
        if practice.airtable_json:
            types_ids = practice.airtable_json['fields'].get('Types', [])
            practice.types.set(list(x for x in types if x.external_id in types_ids))

def _get_added_cultures(json_practice, json_cultures):
    added_cultures = json_practice['fields'].get('Ajout dans la rotation cultures')
    if added_cultures:
        added_cultures = [x for x in json_cultures if x['id'] in added_cultures]
    if not added_cultures:
        return added_cultures

    enum_codes = list(map(lambda x: x['fields']['Enum code'], added_cultures))
    enum_cultures = []
    for code in enum_codes:
        try:
            enum_cultures.append(Culture[code].value)
        except KeyError as _:
            continue
    return enum_cultures


def _get_culture_whitelist(json_practice, json_cultures):
    culture_whitelist = json_practice['fields'].get('Cultures whitelist')
    if culture_whitelist:
        culture_whitelist = [x for x in json_cultures if x['id'] in culture_whitelist]
    if not culture_whitelist:
        return culture_whitelist

    enum_codes = list(map(lambda x: x['fields']['Enum code'], culture_whitelist))
    enum_cultures = []
    for code in enum_codes:
        try:
            enum_cultures.append(Culture[code].value)
        except KeyError as _:
            continue
    return enum_cultures


def _get_mechanism(json_practice, mechanisms):
    mechanism_airtable_ids = json_practice['fields'].get('Marges de manoeuvre')
    if not mechanism_airtable_ids:
        return None
    return next(filter(lambda x: x.external_id in mechanism_airtable_ids, mechanisms), None)


def _get_main_resource(json_practice, resources):
    resource_airtable_ids = json_practice['fields'].get('CTA lien')
    if not resource_airtable_ids:
        return None
    return next(filter(lambda x: x.external_id in resource_airtable_ids, resources), None)


def _get_problems_addressed(json_practice):
    airtable_adressed_problems = json_practice['fields'].get('Problèmes adressés')
    if not airtable_adressed_problems:
        return None

    problems = []
    for airtable_problem in airtable_adressed_problems:
        try:
            problems.append(Problem[airtable_problem].value)
        except KeyError as _:
            continue
    return problems


def _get_weeds(json_practice, json_weeds):
    weeds_ids = json_practice['fields'].get('Adventices whitelist')
    if not weeds_ids:
        return None

    airtable_weeds = list(filter(lambda x: x.get('id') in weeds_ids, json_weeds))
    airtable_weeds_enum_codes = list(map(lambda x: x['fields'].get('Enum code'), airtable_weeds))
    weeds = []
    for code in airtable_weeds_enum_codes:
        try:
            weeds.append(Weed[code].value)
        except KeyError as _:
            continue
    return weeds


def _get_pests(json_practice, json_pests):

    pests_ids = json_practice['fields'].get('Ravageurs whitelist')
    if not pests_ids:
        return None

    airtable_pests = list(filter(lambda x: x.get('id') in pests_ids, json_pests))
    airtable_pests_enum_codes = list(map(lambda x: x['fields'].get('Enum code'), airtable_pests))
    pests = []
    for code in airtable_pests_enum_codes:
        try:
            pests.append(Pest[code].value)
        except KeyError as _:
            continue
    return pests


def _get_department_multipliers(json_practice, json_departments_practices, json_departments):
    departments = json_departments
    departments_practices = json_departments_practices
    practice = json_practice

    concerned_department_practices = list(filter(lambda x: practice['id'] in (x['fields'].get('Pratique') or []), departments_practices))
    if not concerned_department_practices:
        return []

    department_multipliers = []
    for item in concerned_department_practices:
        if not item['fields'].get('Departement'):
            continue

        department_airtable_id = item['fields'].get('Departement')[0]
        airtable_department_entry = next(filter(lambda x: x['id'] == department_airtable_id, departments), None)
        if not airtable_department_entry or not airtable_department_entry['fields'].get('Numéro'):
            continue

        department_number = airtable_department_entry['fields'].get('Numéro')
        multiplier = item['fields'].get('Multiplicateur') or 1

        department_multipliers.append({
            department_number: multiplier
        })

    return department_multipliers


def _get_weed_multipliers(json_practice, json_weeds, json_weed_practices):
    concerned_weed_practices = list(filter(lambda x: json_practice['id'] in (x['fields'].get('Pratique') or []), json_weed_practices))
    if not concerned_weed_practices:
        return []

    weed_multipliers = []
    for item in concerned_weed_practices:
        if not item['fields'].get('Adventice'):
            continue

        weed_airtable_id = item['fields'].get('Adventice')[0]
        airtable_weed_entry = next(filter(lambda x: x['id'] == weed_airtable_id, json_weeds), None)
        if not airtable_weed_entry or not airtable_weed_entry['fields'].get('Enum code'):
            continue

        try:
            weed_enum_number = Weed[airtable_weed_entry['fields'].get('Enum code')].value
            multiplier = item['fields'].get('Multiplicateur') or 1

            weed_multipliers.append({
                weed_enum_number: multiplier
            })
        except KeyError as _:
            continue

    return weed_multipliers

def _get_pest_multipliers(json_practice, json_pests, json_pest_practices):
    concerned_pest_practices = list(filter(lambda x: json_practice['id'] in (x['fields'].get('Pratique') or []), json_pest_practices))
    if not concerned_pest_practices:
        return []

    pest_multipliers = []
    for item in concerned_pest_practices:
        if not item['fields'].get('Ravageur'):
            continue

        pest_airtable_id = item['fields'].get('Ravageur')[0]
        airtable_pest_entry = next(filter(lambda x: x['id'] == pest_airtable_id, json_pests), None)
        if not airtable_pest_entry or not airtable_pest_entry['fields'].get('Enum code'):
            continue

        try:
            pest_enum_number = Pest[airtable_pest_entry['fields'].get('Enum code')].value
            multiplier = item['fields'].get('Multiplicateur') or 1

            pest_multipliers.append({
                pest_enum_number: multiplier
            })
        except KeyError as _:
            continue

    return pest_multipliers


def _get_glyphosate_multipliers(json_practice, json_glyphosate, json_glyphosate_practices):
    concerned_glyphosate_practices = list(filter(lambda x: json_practice['id'] in (x['fields'].get('Pratique') or []), json_glyphosate_practices))
    if not concerned_glyphosate_practices:
        return []

    glyphosate_multipliers = []
    for item in concerned_glyphosate_practices:
        if not item['fields'].get('Glyphosate'):
            continue

        glyphosate_airtable_id = item['fields'].get('Glyphosate')[0]
        airtable_glyphosate_entry = next(filter(lambda x: x['id'] == glyphosate_airtable_id, json_glyphosate), None)
        if not airtable_glyphosate_entry or not airtable_glyphosate_entry['fields'].get('Enum code'):
            continue

        try:
            glyphosate_enum_number = GlyphosateUses[airtable_glyphosate_entry['fields'].get('Enum code')].value
            multiplier = item['fields'].get('Multiplicateur') or 1

            glyphosate_multipliers.append({
                glyphosate_enum_number: multiplier
            })
        except KeyError as _:
            continue

    return glyphosate_multipliers

def _get_culture_multipliers(json_practice, json_cultures, json_culture_practices):
    concerned_culture_practices = list(filter(lambda x: json_practice['id'] in (x['fields'].get('Pratique') or []), json_culture_practices))
    if not concerned_culture_practices:
        return []

    culture_multipliers = []
    for item in concerned_culture_practices:
        if not item['fields'].get('Culture'):
            continue

        culture_airtable_id = item['fields'].get('Culture')[0]
        airtable_culture_entry = next(filter(lambda x: x['id'] == culture_airtable_id, json_cultures), None)
        if not airtable_culture_entry or not airtable_culture_entry['fields'].get('Enum code'):
            continue

        try:
            culture_enum_number = Culture[airtable_culture_entry['fields'].get('Enum code')].value
            multiplier = item['fields'].get('Multiplicateur') or 1

            culture_multipliers.append({
                culture_enum_number: multiplier
            })
        except KeyError as _:
            continue

    return culture_multipliers


def _get_image_url(json_practice):
    if not json_practice['fields'].get('Image principale'):
        return None
    return json_practice['fields'].get('Image principale')[0].get('url')


def _fetch_mechanisms(json_mechanisms):
    mechanisms = []
    for json_mechanism in json_mechanisms:
        mechanisms.append(Mechanism(
            external_id=json_mechanism.get('id'),
            modification_date=timezone.now(),
            airtable_json=json_mechanism,
            airtable_url='https://airtable.com/tbliz8fD7ZaoqIugz/' + json_mechanism.get('id') + '/',
            name=json_mechanism['fields'].get('Name'),
            description=json_mechanism['fields'].get('Description'),
        ))
    return mechanisms


def _fetch_resources(json_resources):
    resources = []

    for json_resource in json_resources:
        resources.append(Resource(
            external_id=json_resource.get('id'),
            modification_date=timezone.now(),
            airtable_json=json_resource,
            airtable_url='https://airtable.com/tblVb2GDuCPGUrt35/' + json_resource.get('id') + '/',
            name=json_resource['fields'].get('Nom'),
            description=json_resource['fields'].get('Description'),
            resource_type=_get_resource_type(json_resource),
            url=json_resource['fields'].get('Url'),
        ))
    return resources

def _get_resource_type(json_resource):
    resource_type = json_resource['fields'].get('Type')
    if resource_type == 'PDF':
        return ResourceType.PDF.value
    if resource_type == 'Site web':
        return ResourceType.SITE_WEB.value
    if resource_type == 'Vidéo':
        return ResourceType.VIDEO.value
    return None

def _get_airtable_data(url):
    time.sleep(settings.AIRTABLE_REQUEST_INTERVAL_SECONDS) # lazy way to throttle, sorry
    base_url = 'https://api.airtable.com/v0/appqlHvlvvxHDkQNY/'
    headers = {
        'Authorization': 'Bearer ' + settings.AIRTABLE_API_KEY,
        'Accept': 'application/json',
    }

    response = requests.get(base_url + url, headers=headers)
    if not response.status_code == 200:
        print('Terrible error while fetching: ' + url)
        return {}
    return json.loads(response.text)['records']

import time
import json
import requests
from django.conf import settings
from django.utils import timezone
from data.models import Problem, PracticeType, Weed, Pest, Resource, ResourceType, GlyphosateUses
from data.models import Culture, Practice, PracticeGroup, Mechanism, PracticeTypeCategory
from data.airtablevalidators import validate_practices, validate_practice_types, validate_weeds
from data.airtablevalidators import validate_pests, validate_cultures, validate_glyphosate_uses
from data.airtablevalidators import validate_resources


class AirtableAdapter:
    """
    Updates the database from Airtable records.
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

        json_resources = _get_airtable_data('Liens?view=Grid%20view')
        errors += validate_resources(json_resources)

        json_culture_practices = _get_airtable_data('Pratiques%2FCultures?view=Grid%20view')
        json_departments_practices = _get_airtable_data('Pratiques%2FDepartements?view=Grid%20view')
        json_departments = _get_airtable_data('Departements?view=Grid%20view')
        json_weed_practices = _get_airtable_data('Pratiques%2FAdventices?view=Grid%20view') # TODO: add validation
        json_pest_practices = _get_airtable_data('Pratiques%2FRavageurs?view=Grid%20view') # TODO: add validation
        json_glyphosate_practices = _get_airtable_data('Pratiques%2FGlyphosate?view=Grid%20view')
        json_practice_groups = _get_airtable_data('Familles?view=Grid%20view')
        json_mechanisms = _get_airtable_data('Marges%20de%20manoeuvre?view=Grid%20view')

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

        practices = _create_practice_models(json_practices, json_culture_practices, json_departments_practices,
                                            json_departments, json_glyphosate, json_glyphosate_practices, mechanisms,
                                            resources, json_practice_types, json_weeds, json_weed_practices, json_pests, json_pest_practices)

        practice_groups = _create_pratice_group_models(json_practice_groups)
        practice_types = _create_practice_type_models(json_practice_types)

        weeds = _create_weed_models(json_weeds)
        pests = _create_pest_models(json_pests)
        cultures = _create_culture_models(json_cultures)

        PracticeGroup.objects.all().delete()
        for practice_group in practice_groups:
            practice_group.save()

        PracticeType.objects.all().delete()
        for practice_type in practice_types:
            practice_type.save()

        Weed.objects.all().delete()
        for weed in weeds:
            weed.save()

        Pest.objects.all().delete()
        for pest in pests:
            pest.save()

        Practice.objects.all().delete()
        for practice in practices:
            practice.save()

        Culture.objects.all().delete()
        for culture in cultures:
            culture.save()

        _link_practices_with_groups(practices, practice_groups)
        _link_practices_with_resources(practices, resources)
        _link_practices_with_types(practices, practice_types)

        return errors


def _create_practice_models(json_practices, json_culture_practices, json_departments_practices,
                            json_departments, json_glyphosate, json_glyphosate_practices, mechanisms,
                            resources, json_practice_types, json_weeds, json_weed_practices, json_pests, json_pest_practices):
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
            added_cultures=_get_added_cultures(json_practice),
            culture_whitelist=_get_culture_whitelist(json_practice),
            problems_addressed=_get_problems_addressed(json_practice),
            image_url=_get_image_url(json_practice),
            department_multipliers=_get_department_multipliers(json_practice, json_departments_practices, json_departments),
            glyphosate_multipliers=_get_glyphosate_multipliers(json_practice, json_glyphosate, json_glyphosate_practices),
            culture_multipliers=_get_culture_multipliers(json_practice, json_culture_practices),
            needs_shallow_tillage=get_shallow_tillage_need(json_practice, json_practice_types),
            needs_deep_tillage=get_deep_tillage_need(json_practice, json_practice_types),
            weed_multipliers=_get_weed_multipliers(json_practice, json_weeds, json_weed_practices),
            pest_multipliers=_get_pest_multipliers(json_practice, json_pests, json_pest_practices),
            weed_whitelist_external_ids=json_practice['fields'].get('Adventices whitelist', []),
            pest_whitelist_external_ids=json_practice['fields'].get('Ravageurs whitelist', []),
            modification_date=timezone.now(),
        ))

    return practices


def _create_pratice_group_models(json_practice_groups):

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


def _create_weed_models(json_weeds):
    weeds = []
    for json_weed in json_weeds:

        try:
            nature = Weed.WeedNature[json_weed['fields'].get('type')]
        except KeyError as _:
            nature = None

        weeds.append(Weed(
            external_id=json_weed.get('id'),
            airtable_json=json_weed,
            modification_date=timezone.now(),
            display_text=json_weed['fields'].get('Name'),
            description=json_weed['fields'].get('Description'),
            nature=nature.value,
        ))
    return weeds


def _create_pest_models(json_pests):
    pests = []
    for json_pest in json_pests:
        pests.append(Pest(
            external_id=json_pest.get('id'),
            airtable_json=json_pest,
            modification_date=timezone.now(),
            display_text=json_pest['fields'].get('Name'),
            description=json_pest['fields'].get('Description'),
        ))
    return pests

def _create_culture_models(json_cultures):
    cultures = []
    for json_culture in json_cultures:
        culture = Culture(
            external_id=json_culture.get('id'),
            airtable_json=json_culture,
            modification_date=timezone.now(),
            display_text=json_culture['fields'].get('Name'),
        )

        periodes_de_semis = json_culture['fields'].get('période de semis')
        if periodes_de_semis:
            try:
                culture.sowing_period = Culture.CulturesSowingPeriod[periodes_de_semis[0]].value
            except KeyError as _:
                pass

        mois_semis = json_culture['fields'].get('mois semis')
        if mois_semis:
            mois_codes = []
            for mois in mois_semis:
                try:
                    mois_codes.append(Culture.CulturesSowingMonth[mois].value)
                except KeyError as _:
                    pass
            culture.sowing_month = mois_codes
        cultures.append(culture)
    return cultures

def _create_practice_type_models(json_practice_types):

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

def _get_weed_multipliers(json_practice, json_weeds, json_weed_practices):
    concerned_weed_practices = list(filter(lambda x: json_practice['id'] in (x['fields'].get('Pratique') or []), json_weed_practices))
    if not concerned_weed_practices:
        return[]

    weed_multipliers = []
    for weed_practice in concerned_weed_practices:
        if not weed_practice['fields'].get('Adventice') or not weed_practice['fields'].get('Multiplicateur'):
            continue
        weed_airtable_id = weed_practice['fields'].get('Adventice')[0]
        weed = next(filter(lambda x: x['id'] == weed_airtable_id, json_weeds), None)
        weed_multipliers.append({
            weed['id']: weed_practice['fields'].get('Multiplicateur') or 1
        })

    return weed_multipliers

def _get_pest_multipliers(json_practice, json_pests, json_pest_practices):
    concerned_pest_practices = list(filter(lambda x: json_practice['id'] in (x['fields'].get('Pratique') or []), json_pest_practices))
    if not concerned_pest_practices:
        return []

    pest_multipliers = []
    for pest_practice in concerned_pest_practices:
        if not pest_practice['fields'].get('Ravageur') or not pest_practice['fields'].get('Multiplicateur'):
            continue
        pest_airtable_id = pest_practice['fields'].get('Ravageur')[0]
        pest = next(filter(lambda x: x['id'] == pest_airtable_id, json_pests), None)
        pest_multipliers.append({
            pest['id']: pest_practice['fields'].get('Multiplicateur') or 1
        })

    return pest_multipliers


def _get_added_cultures(json_practice):
    added_cultures = json_practice['fields'].get('Ajout dans la rotation cultures')
    return added_cultures


def _get_culture_whitelist(json_practice):
    culture_whitelist = json_practice['fields'].get('Cultures whitelist')
    return culture_whitelist


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

def _get_culture_multipliers(json_practice, json_culture_practices):
    concerned_culture_practices = list(filter(lambda x: json_practice['id'] in (x['fields'].get('Pratique') or []), json_culture_practices))
    if not concerned_culture_practices:
        return []

    culture_multipliers = []
    for item in concerned_culture_practices:
        if not item['fields'].get('Culture'):
            continue

        culture_airtable_id = item['fields'].get('Culture')[0]
        multiplier = item['fields'].get('Multiplicateur') or 1
        culture_multipliers.append({
            culture_airtable_id: multiplier
        })

    return culture_multipliers


def get_shallow_tillage_need(json_practice, json_practice_types):
    practice_type_ids = json_practice['fields'].get('Types')
    practice_types = list(filter(lambda x: x['id'] in practice_type_ids, json_practice_types))
    for practice_type in practice_types:
        if practice_type['fields'].get('Enum code') == PracticeTypeCategory.TRAVAIL_DU_SOL.name:
            return True
    return False


def get_deep_tillage_need(json_practice, json_practice_types):
    practice_type_ids = json_practice['fields'].get('Types')
    practice_types = list(filter(lambda x: x['id'] in practice_type_ids, json_practice_types))
    for practice_type in practice_types:
        if practice_type['fields'].get('Enum code') == PracticeTypeCategory.TRAVAIL_PROFOND.name:
            return True
    return False


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

def _get_airtable_data(url, offset=None):
    time.sleep(settings.AIRTABLE_REQUEST_INTERVAL_SECONDS) # lazy way to throttle, sorry
    base_url = 'https://api.airtable.com/v0/appqlHvlvvxHDkQNY/'
    headers = {
        'Authorization': 'Bearer ' + settings.AIRTABLE_API_KEY,
        'Accept': 'application/json',
    }

    url_params = ''
    if offset:
        divider = '&' if '?' in url else '?'
        url_params = '%soffset=%s' % (divider, offset)

    response = requests.get(base_url + url + url_params, headers=headers)
    if not response.status_code == 200:
        print('Terrible error while fetching: ' + url)
        return {}
    json_response = json.loads(response.text)
    records = json_response['records']
    offset = json_response.get('offset')
    if offset:
        return records + _get_airtable_data(url, offset)
    return records

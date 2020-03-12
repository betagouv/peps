from django.conf import settings
from data.models import PracticeType, Weed, Pest, Resource
from data.models import Culture, Practice, PracticeGroup, Mechanism, Category
from data.utils import _get_airtable_data
from data.airtablevalidators import validate_practices, validate_practice_types, validate_weeds
from data.airtablevalidators import validate_pests, validate_cultures, validate_glyphosate_uses
from data.airtablevalidators import validate_resources, validate_categories, validate_weed_practices
from data.airtablevalidators import validate_pest_practices, validate_culture_practices, validate_department_practices
from data.airtablevalidators import validate_departments, validate_glyphosate_practices, validate_practice_groups
from data.airtablevalidators import validate_mechanisms, validate_resource_images


class PracticesAirtableAdapter:
    """
    Updates the database from Airtable records linked to the practices.
    """

    @staticmethod
    def update():
        """
        We completely replace whatever we have in the DB for
        the new information. Eventually we may want to only replace
        the changed ones.

        If there are errors, an array of them will be returned.
        """
        errors = []
        practices_base = settings.AIRTABLE_PRACTICES_BASE

        json_practices = _get_airtable_data('Pratiques?view=Grid%20view', practices_base)
        errors += validate_practices(json_practices)

        json_practice_types = _get_airtable_data('Types%20de%20pratique?view=Grid%20view', practices_base)
        errors += validate_practice_types(json_practice_types)

        json_weeds = _get_airtable_data('Adventices?view=Grid%20view', practices_base)
        errors += validate_weeds(json_weeds)

        json_pests = _get_airtable_data('Ravageurs?view=Grid%20view', practices_base)
        errors += validate_pests(json_pests)

        json_cultures = _get_airtable_data('Cultures?view=Grid%20view', practices_base)
        errors += validate_cultures(json_cultures)

        json_glyphosate = _get_airtable_data('Glyphosate?view=Grid%20view', practices_base)
        errors += validate_glyphosate_uses(json_glyphosate)

        json_resources = _get_airtable_data('Liens?view=Grid%20view', practices_base)
        errors += validate_resources(json_resources)

        json_resource_images = _get_airtable_data('logos?view=Grid%20view', practices_base)
        errors += validate_resource_images(json_resource_images)

        json_categories = _get_airtable_data('Categories?view=Grid%20view', practices_base)
        errors += validate_categories(json_categories)

        json_weed_practices = _get_airtable_data('Pratiques%2FAdventices?view=Grid%20view', practices_base)
        errors += validate_weed_practices(json_weed_practices)

        json_pest_practices = _get_airtable_data('Pratiques%2FRavageurs?view=Grid%20view', practices_base)
        errors += validate_pest_practices(json_pest_practices)

        json_culture_practices = _get_airtable_data('Pratiques%2FCultures?view=Grid%20view', practices_base)
        errors += validate_culture_practices(json_culture_practices)

        json_departments_practices = _get_airtable_data('Pratiques%2FDepartements?view=Grid%20view', practices_base)
        errors += validate_department_practices(json_departments_practices)

        json_departments = _get_airtable_data('Departements?view=Grid%20view', practices_base)
        errors += validate_departments(json_departments)

        json_glyphosate_practices = _get_airtable_data('Pratiques%2FGlyphosate?view=Grid%20view', practices_base)
        errors += validate_glyphosate_practices(json_glyphosate_practices)

        json_practice_groups = _get_airtable_data('Familles?view=Grid%20view', practices_base)
        errors += validate_practice_groups(json_practice_groups)

        json_mechanisms = _get_airtable_data('Marges%20de%20manoeuvre?view=Grid%20view', practices_base)
        errors += validate_mechanisms(json_mechanisms)

        has_fatal_errors = any(x.fatal for x in errors)
        if has_fatal_errors:
            return errors

        mechanisms = [Mechanism.create_from_airtable(x) for x in json_mechanisms]
        Mechanism.objects.all().delete()
        for mechanism in mechanisms:
            mechanism.save()

        categories = [Category.create_from_airtable(x) for x in json_categories]
        Category.objects.all().delete()
        for category in categories:
            category.save()

        json_resource_images.sort(key=lambda x: len(x['fields'].get('URL_principal')), reverse=True)
        resources = [Resource.create_from_airtable(x, json_resource_images) for x in json_resources]
        Resource.objects.all().delete()
        for resource in resources:
            resource.save()

        practice_groups = [PracticeGroup.create_from_airtable(x) for x in json_practice_groups]
        PracticeGroup.objects.all().delete()
        for practice_group in practice_groups:
            practice_group.save()

        practice_types = [PracticeType.create_from_airtable(x) for x in json_practice_types]
        PracticeType.objects.all().delete()
        for practice_type in practice_types:
            practice_type.save()

        weeds = [Weed.create_from_airtable(x) for x in json_weeds]
        Weed.objects.all().delete()
        for weed in weeds:
            weed.save()

        pests = [Pest.create_from_airtable(x) for x in json_pests]
        Pest.objects.all().delete()
        for pest in pests:
            pest.save()

        accepted_sectors = ['Grande culture']
        cultures = [Culture.create_from_airtable(x) for x in json_cultures if x['fields'].get('Filière') in accepted_sectors]
        Culture.objects.all().delete()
        for culture in cultures:
            culture.save()

        practices = [Practice.create_from_airtable(x, json_culture_practices, json_departments_practices,
                                                   json_departments, json_glyphosate, json_glyphosate_practices,
                                                   mechanisms, resources, json_practice_types, json_weeds,
                                                   json_weed_practices, json_pests, json_pest_practices) for x in json_practices]
        Practice.objects.all().delete()
        for practice in practices:
            practice.save()

        _link_practices_with_groups(practices, practice_groups)
        _link_practices_with_resources(practices, resources)
        _link_practices_with_types(practices, practice_types)
        _link_practices_with_categories(practices, categories)

        return errors

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

def _link_practices_with_categories(practices, categories):
    for category in categories:
        category.practices.set(list(x for x in practices if x.external_id in category.practice_external_ids))

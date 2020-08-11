import uuid
from django.db import models
from django.utils import timezone
from django.contrib.postgres.fields import ArrayField
from django.db.models import JSONField
from data.utils import get_airtable_media_name, get_airtable_media_content_file
from .practicegroup import PracticeGroup
from .practicetype import PracticeType, PracticeTypeCategory
from .mechanism import Mechanism
from .resource import Resource
from .problem import Problem
from .glyphosateuses import GlyphosateUses

class Practice(models.Model):
    """
    This model represents an agricultural practice that we may suggest to
    the user.
    """

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    external_id = models.CharField(max_length=100)
    modification_date = models.DateTimeField(auto_now=True)
    creation_date = models.DateTimeField(default=timezone.now)
    image = models.ImageField(null=True)

    airtable_json = JSONField(null=True, blank=True)
    airtable_url = models.TextField(null=True, blank=True)

    title = models.TextField(null=True, blank=True)
    short_title = models.TextField()
    description = models.TextField(null=True, blank=True)

    mechanism = models.ForeignKey(Mechanism, null=True, blank=True, on_delete=models.SET_NULL)

    equipment = models.TextField(null=True, blank=True)
    schedule = models.TextField(null=True, blank=True)
    impact = models.TextField(null=True, blank=True)
    additional_benefits = models.TextField(null=True, blank=True)
    success_factors = models.TextField(null=True, blank=True)

    needs_shallow_tillage = models.BooleanField(blank=True, null=True)
    needs_deep_tillage = models.BooleanField(blank=True, null=True)
    weed_whitelist_external_ids = ArrayField(models.TextField(), default=list)
    pest_whitelist_external_ids = ArrayField(models.TextField(), default=list)
    balances_sowing_period = models.BooleanField(blank=True, null=True)

    # Practices can have one main resource and several secondary ones
    main_resource_label = models.TextField(null=True, blank=True)
    main_resource = models.ForeignKey(Resource, null=True, blank=True, on_delete=models.SET_NULL, related_name="main_practices", related_query_name="main_practice",)
    secondary_resources = models.ManyToManyField(Resource)

    # A practice can be part of practice groups - which are groups that
    # refer to the same action but with different levels of specificity.
    # We should not propose practices from the same practice group.
    practice_groups = models.ManyToManyField(PracticeGroup)

    # Whether or not the practice needs tillage (travail du sol)
    needs_tillage = models.BooleanField(null=True)

    # Whether or not the practice needs livestock
    needs_livestock = models.BooleanField(null=True)

    # If greater than 1, the practice will be boosted if the user has livestock
    # or the possibility to monetize selling animal food. If lower than 1, the
    # practice will be penalized if the user has livestock. A value of 1 does not
    # modify the value of this practice in presence of livestock
    livestock_multiplier = models.DecimalField(null=True, max_digits=7, decimal_places=6)

    # If greater than 1, the practice will be boosted if the user has access
    # to a direct end-consumer sale. If lower than 1, the practice will be penalized
    # if the user has access to end-consumer sale. A value of 1 does not
    # modify the value of this practice in presence of end-consumer sale markets.
    direct_sale_multiplier = models.DecimalField(null=True, max_digits=7, decimal_places=6)

    # The degree at which the practice is precise (0 to 1) - meaning how many decisions must
    # the user take on their own in order to implement this practice. A vague practice
    # e.g., "Make use of better equipment" will have a low precision, whereas a
    # descriptive practice "Make use of a Cataya mechanic seeder combined with a rotative KE
    # to place the corn seeds at 12cm apart from each other" will have a high precision value.
    precision = models.DecimalField(null=True, max_digits=7, decimal_places=6)

    # The degree at which the practice is difficult (0 to 1) - meaning how high is the barrier
    # on the user's side in order to implement this practice.
    difficulty = models.DecimalField(null=True, max_digits=7, decimal_places=6)

    # If this practice adresses particular types of agriculture problem specified in the
    # Problem Enum, this field will store these adressed problems.
    problems_addressed = ArrayField(models.IntegerField(), blank=True, null=True)

    # If this practice corresponds to types available in the PracticeType enum, this field will
    # store them.
    types = models.ManyToManyField(PracticeType)

    # The following fields are multipliers and will boost or handicap the practice depending
    # on the value. A value larger than 1 will boost the practice, whereas a value lower than 1
    # will handicap it. A value equal to 1 will not make a difference.

    # E.g., [{'75': 1.003}, {'69': 0.7329}]
    department_multipliers = ArrayField(JSONField(), blank=True, null=True)

    # E.g., [{1: 1.003}, {5: 0.7329}]
    glyphosate_multipliers = ArrayField(JSONField(), blank=True, null=True)

    # E.g., [{'ARGILEUX': 1.0024}, {'LIMONEUX': 0.6362}]
    soil_type_multipliers = ArrayField(JSONField(), blank=True, null=True)

    # E.g., [{'ARGILEUX': 1.0024}, {'LIMONEUX': 0.6362}]
    soil_type_multipliers = ArrayField(JSONField(), blank=True, null=True)

    # E.g., [{'ARGILEUX': 1.0024}, {'LIMONEUX': 0.6362}]
    soil_type_multipliers = ArrayField(JSONField(), blank=True, null=True)

    # Uses external ID as key
    # E.g., [{'recjzIBqwGkton9Ed': 1.0024}, {'recjzIAuvEkton9Ed': 0.6362}]
    weed_multipliers = ArrayField(JSONField(), blank=True, null=True)

    # Uses external ID as key
    # E.g., [{'recjzIBqwGkton9Ed': 1.0024}, {'recjzIAuvEkton9Ed': 0.6362}]
    pest_multipliers = ArrayField(JSONField(), blank=True, null=True)

    # If this practice involves adding new cultures to the rotation, this field specifies which
    # cultures are being added. These are culture external IDs.
    added_cultures = ArrayField(models.TextField(), blank=True, null=True)

    # If this practice is relevant only for certain types of cultures, they should be specified
    # here. If the practice could be applied to any kind of culture this field should remain
    # empty. These are culture external IDs.
    culture_whitelist = ArrayField(models.TextField(), blank=True, null=True)

    # E.g., [{'recjzIAuvEkton9Ed': 1.003}, {'recjzIArvEkton9Ds': 0.7329}]
    culture_multipliers = ArrayField(JSONField(), blank=True, null=True)


    @staticmethod
    def create_from_airtable(airtable_json, json_culture_practices, json_departments_practices,
                             json_departments, json_glyphosate, json_glyphosate_practices, mechanisms,
                             resources, json_practice_types, json_weeds, json_weed_practices, json_pests, json_pest_practices):
        fields = airtable_json['fields']
        mechanism_external_ids = fields.get('Marges de manoeuvre', [])
        resource_external_ids = fields.get('CTA lien', [])
        practice_types = [x for x in json_practice_types if x['id'] in fields.get('Types')]

        needs_shallow_tillage = any([x for x in practice_types if x['fields'].get('Enum code') == PracticeTypeCategory.TRAVAIL_DU_SOL.name])
        needs_deep_tillage = any([x for x in practice_types if x['fields'].get('Enum code') == PracticeTypeCategory.TRAVAIL_PROFOND.name])

        practice = Practice(
            external_id=airtable_json.get('id'),
            mechanism=next((x for x in mechanisms if x.external_id in mechanism_external_ids), None),
            main_resource=next((x for x in resources if x.external_id in resource_external_ids), None),
            main_resource_label=fields.get('CTA title'),
            airtable_json=airtable_json,
            airtable_url='https://airtable.com/tblobpdQDxkzcllWo/' + airtable_json.get('id') + '/',
            title=fields.get('Nom').strip(),
            short_title=fields.get('Nom court').strip(),
            description=fields.get('Description'),
            equipment=fields.get('Matériel'),
            schedule=fields.get('Période de travail'),
            impact=fields.get('Impact'),
            additional_benefits=fields.get('Bénéfices supplémentaires'),
            success_factors=fields.get('Facteur clé de succès'),
            needs_tillage=fields.get('Nécessite travail du sol', False),
            livestock_multiplier=fields.get('Élevage multiplicateur'),
            needs_livestock=fields.get('Élevage nécessaire', False),
            balances_sowing_period=fields.get('Équilibre période semis', False),
            direct_sale_multiplier=fields.get('Vente directe multiplicateur'),
            precision=fields.get('Précision'),
            difficulty=fields.get('Difficulté'),
            added_cultures=fields.get('Ajout dans la rotation cultures'),
            culture_whitelist=fields.get('Cultures whitelist'),
            problems_addressed=Practice._get_problems_addressed(airtable_json),
            department_multipliers=Practice._get_department_multipliers(airtable_json, json_departments_practices, json_departments),
            glyphosate_multipliers=Practice._get_glyphosate_multipliers(airtable_json, json_glyphosate, json_glyphosate_practices),
            culture_multipliers=Practice._get_culture_multipliers(airtable_json, json_culture_practices),
            needs_shallow_tillage=needs_shallow_tillage,
            needs_deep_tillage=needs_deep_tillage,
            weed_multipliers=Practice._get_weed_multipliers(airtable_json, json_weeds, json_weed_practices),
            pest_multipliers=Practice._get_pest_multipliers(airtable_json, json_pests, json_pest_practices),
            weed_whitelist_external_ids=fields.get('Adventices whitelist', []),
            pest_whitelist_external_ids=fields.get('Ravageurs whitelist', []),
        )
        image_name = get_airtable_media_name(airtable_json, 'Image principale')
        image_content_file = get_airtable_media_content_file(airtable_json, 'Image principale')
        if image_name and image_content_file:
            practice.image.save(image_name, image_content_file, save=True)
        return practice


    @staticmethod
    def _get_problems_addressed(airtable_json):
        fields = airtable_json['fields']
        airtable_adressed_problems = fields.get('Problèmes adressés', [])
        problems = []
        for airtable_problem in airtable_adressed_problems:
            try:
                problems.append(Problem[airtable_problem].value)
            except KeyError as _:
                continue
        return problems


    @staticmethod
    def _get_department_multipliers(airtable_json, json_departments_practices, json_departments):
        departments = json_departments
        departments_practices = json_departments_practices
        practice = airtable_json

        concerned_department_practices = list(filter(lambda x: practice['id'] in (x['fields'].get('Pratique') or []), departments_practices))
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

    @staticmethod
    def _get_glyphosate_multipliers(airtable_json, json_glyphosate, json_glyphosate_practices):
        concerned_glyphosate_practices = list(filter(lambda x: airtable_json['id'] in (x['fields'].get('Pratique') or []), json_glyphosate_practices))
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

    @staticmethod
    def _get_culture_multipliers(airtable_json, json_culture_practices):
        concerned_culture_practices = list(filter(lambda x: airtable_json['id'] in (x['fields'].get('Pratique') or []), json_culture_practices))
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


    @staticmethod
    def _get_weed_multipliers(airtable_json, json_weeds, json_weed_practices):
        concerned_weed_practices = list(filter(lambda x: airtable_json['id'] in (x['fields'].get('Pratique') or []), json_weed_practices))
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


    @staticmethod
    def _get_pest_multipliers(airtable_json, json_pests, json_pest_practices):
        concerned_pest_practices = list(filter(lambda x: airtable_json['id'] in (x['fields'].get('Pratique') or []), json_pest_practices))
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
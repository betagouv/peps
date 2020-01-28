import uuid
from django.db import models
from django.utils import timezone
from django.contrib.postgres.fields import JSONField, ArrayField
from .practicegroup import PracticeGroup
from .practicetype import PracticeType
from .mechanism import Mechanism
from .resource import Resource

class Practice(models.Model):
    """
    This model represents an agricultural practice that we may suggest to
    the user.
    """

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    external_id = models.CharField(max_length=100)
    modification_date = models.DateTimeField()
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

    airtable_image_url = models.TextField(null=True, blank=True)

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

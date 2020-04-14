import datetime
from decimal import Decimal
from dateutil import parser
from django.conf import settings
from django.contrib.auth import get_user_model
from data.models import Farmer, Experiment
from data.utils import _get_airtable_data
from data.airtablevalidators import validate_farmers, validate_experiments

class ExperimentsAirtableAdapter:
    """
    Updates the database from Airtable records linked to the experiments.
    """

    @staticmethod
    def update():
        """
        We completely replace whatever we have in the DB tables for
        the new information.

        If there are errors, an array of them will be returned.
        """
        errors = []
        base = settings.AIRTABLE_XP_BASE

        json_farmers = _get_airtable_data('Agriculteur?view=Grid%20view', base)
        json_farmers = list(filter(lambda x: x['fields'].get('Validation'), json_farmers))
        errors += validate_farmers(json_farmers)

        json_experiments = _get_airtable_data('XP?view=Grid%20view', base)
        json_experiments = list(filter(lambda x: x['fields'].get('Validation'), json_experiments))
        errors += validate_experiments(json_experiments)

        has_fatal_errors = any(x.fatal for x in errors)
        if has_fatal_errors:
            return errors

        # Farmers added in Airtable should be able to modify their information.
        # We should have users for each of them who are able to view and edit their info.
        # farmers = filter(lambda x: x, farmers) # Take those who have been modified recently only

        for json_farmer in json_farmers:
            airtable_id = json_farmer.get('id')
            airtable_modification_date = json_farmer['fields'].get('Last Modified') if json_farmer.get('fields') else None
            if not airtable_id or not airtable_modification_date:
                continue

            (farmer, created) = Farmer.objects.get_or_create(external_id=airtable_id, defaults={'lat': Decimal(0.0), 'lon': Decimal(0.0)})

            if created or parser.isoparse(airtable_modification_date) > farmer.modification_date:
                farmer.update_from_airtable(json_farmer)
                farmer.save()

            if farmer.email and not get_user_model().objects.filter(email=farmer.email).first():
                get_user_model().objects.create_user(email=farmer.email, username=farmer.email, password=get_user_model().objects.make_random_password())


        for json_experiment in json_experiments:
            airtable_id = json_experiment.get('id')
            airtable_modification_date = json_experiment['fields'].get('Last Modified') if json_experiment.get('fields') else None
            if not airtable_id or not airtable_modification_date:
                continue

            (experiment, created) = Experiment.objects.get_or_create(external_id=airtable_id, defaults={'name': ''})

            if created or parser.isoparse(airtable_modification_date) > experiment.modification_date:
                experiment.update_from_airtable(json_experiment)
                farmer_external_id = experiment.airtable_json['fields'].get('Agriculteur')[0]
                experiment.farmer = Farmer.objects.filter(external_id=farmer_external_id).first()
                experiment.save()

        return errors

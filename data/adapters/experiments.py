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
        # json_farmers = list(filter(lambda x: x['fields'].get('Validation'), json_farmers))
        errors += validate_farmers(json_farmers)

        json_experiments = _get_airtable_data('XP?view=Grid%20view', base)
        # json_experiments = list(filter(lambda x: x['fields'].get('Validation'), json_experiments))
        errors += validate_experiments(json_experiments)

        has_fatal_errors = any(x.fatal for x in errors)
        if has_fatal_errors:
            return errors

        for json_farmer in json_farmers:
            airtable_id = json_farmer.get('id')
            airtable_modification_date = json_farmer['fields'].get('Last Modified') if json_farmer.get('fields') else None
            if not airtable_id or not airtable_modification_date:
                continue

            defaults = {'lat': Decimal(0.0), 'lon': Decimal(0.0), 'approved': json_farmer['fields'].get('validation', False)}
            (farmer, created) = Farmer.objects.get_or_create(external_id=airtable_id, defaults=defaults)

            # email_matches = json_farmer['fields'].get('Adresse email') == farmer.email

            # if created or parser.isoparse(airtable_modification_date) > farmer.modification_date or not email_matches:
            farmer.update_from_airtable(json_farmer)
            farmer.save()

            if farmer.email:
                farmer_email = farmer.email.strip().lower()
                if not get_user_model().objects.filter(email=farmer_email).first():
                    random_password = get_user_model().objects.make_random_password()
                    get_user_model().objects.create_user(email=farmer_email, username=farmer_email, password=random_password)

                farmer.user = get_user_model().objects.filter(email=farmer_email).first()
                farmer.save()


        for json_experiment in json_experiments:
            airtable_id = json_experiment.get('id')
            airtable_modification_date = json_experiment['fields'].get('Last Modified') if json_experiment.get('fields') else None
            if not airtable_id or not airtable_modification_date:
                continue

            defaults = {'name': airtable_id, 'approved': json_experiment['fields'].get('Validation', False)}
            (experiment, created) = Experiment.objects.get_or_create(external_id=airtable_id, defaults=defaults)

            # if created or parser.isoparse(airtable_modification_date) > experiment.modification_date:
            experiment.update_from_airtable(json_experiment)
            farmer_external_id = experiment.airtable_json['fields'].get('Agriculteur')[0]
            experiment.farmer = Farmer.objects.filter(external_id=farmer_external_id).first()
            experiment.save()

        return errors

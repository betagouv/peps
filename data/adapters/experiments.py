from django.conf import settings
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

        farmers = [Farmer.create_from_airtable(x) for x in json_farmers]
        Farmer.objects.all().delete()
        for farmer in farmers:
            farmer.save()

        experiments = [Experiment.create_from_airtable(x) for x in json_experiments]
        Experiment.objects.all().delete()
        for experiment in experiments:
            experiment.save()
            experiment.assign_images_from_airtable()

        _link_experiments_with_farmers(experiments)

        return errors

def _link_experiments_with_farmers(experiments):
    for experiment in experiments:
        if experiment.airtable_json:
            farmer_external_id = experiment.airtable_json['fields'].get('Agriculteur')[0]
            experiment.farmer = Farmer.objects.filter(external_id=farmer_external_id).first()
            experiment.save()

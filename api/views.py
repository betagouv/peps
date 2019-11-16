import dateutil.parser
from mailjet_rest import Client
from django.http import HttpResponse, JsonResponse
from django.conf import settings
from rest_framework.renderers import JSONRenderer
from rest_framework.views import APIView
from rest_framework.generics import CreateAPIView
from rest_framework import permissions, authentication
from rest_framework_api_key.permissions import HasAPIKey
import asana
from data.adapters import AirtableAdapter
from data.models import Practice, GroupCount, RefererCount
from api.engine import Engine
from api.serializers import ResponseSerializer, DiscardActionSerializer
from api.formschema import get_form_schema
from api.models import Response

# For the moment, we will authorize access to this endpoint in one of these two situations:
# - The user logged in and has a session (which identifies a user)
# - The call has an API key (which identifies projects, not users)
class RankingsApiView(APIView):
    """
    This view will return a list of practice IDs that
    correspond to the form from FormView.
    """
    authentication_classes = [authentication.SessionAuthentication]
    permission_classes = [HasAPIKey | permissions.IsAuthenticated]

    def post(self, request):
        post_data = request.data
        practices, suggestions = RankingsApiView.get_results(
            post_data.get('answers'),
            post_data.get('practice_blacklist', []),
            post_data.get('type_blacklist', [])
        )

        response = Response(practices, suggestions)
        data = JSONRenderer().render(ResponseSerializer(response).data)

        return HttpResponse(data, content_type="application/json")

    @staticmethod
    def get_results(answers, practice_blacklist, type_blacklist):
        engine = Engine(answers, practice_blacklist, type_blacklist)
        practices = engine.calculate_results()
        suggestions = engine.get_suggestions(practices)
        return (practices, suggestions)


class RefreshDataApiView(APIView):
    """
    This view will return a list of practice IDs that
    correspond to the form from FormView.
    """
    authentication_classes = [authentication.SessionAuthentication]
    permission_classes = [permissions.IsAuthenticated | HasAPIKey]

    def post(self, request):
        errors = AirtableAdapter.update_practices()
        has_fatal_errors = any(x.fatal for x in errors)

        json_errors = [{'message': x.message, 'fatal': x.fatal, 'url': x.url} for x in errors]
        return JsonResponse({'success': not has_fatal_errors, 'errors': json_errors})


class FormSchemaView(APIView):
    """
    This view will return the schema needed for rendering
    the form in the front-end
    """
    authentication_classes = [authentication.SessionAuthentication]
    permission_classes = [permissions.IsAuthenticated | HasAPIKey]

    def get(self, request):
        return JsonResponse(get_form_schema())


class SendEmailView(APIView):
    """
    This view will send an email to the specified address
    containing the specified practices. Uses Mailjet. Unfortunately
    due to several bugs in Mailjet we have to send exactly three practices.
    """
    authentication_classes = [authentication.SessionAuthentication]
    permission_classes = [permissions.IsAuthenticated | HasAPIKey]

    def post(self, request):
        email = request.data.get('email')
        practice_external_ids = request.data.get('practices', [])
        first_name = request.data.get('first_name')
        problem = request.data.get('problem')

        if len(practice_external_ids) != 3:
            return JsonResponse({}, status=400)

        suggestions = [Practice.objects.filter(external_id=x).first() for x in practice_external_ids]

        if None in suggestions:
            return JsonResponse({}, status=400)

        mailjet_variables = SendEmailView._get_mailjet_variables(suggestions, first_name, problem)

        data = {
            'Messages': [{
                "From": {
                    "Email": "peps@beta.gouv.fr",
                    "Name": "Peps"
                },
                "To": [{
                    "Email": email,
                    "Name": first_name,
                }],
                "TemplateID": 1021512,
                "TemplateLanguage": True,
                "Subject": "Récapitulatif des pratiques suggérées",
                "Variables": mailjet_variables,
            }]
        }
        result = SendEmailView._send_email(data)
        return JsonResponse(result.json(), status=result.status_code)

    @staticmethod
    def _send_email(data):
        api_key = settings.MJ_APIKEY_PUBLIC[0]
        api_secret = settings.MJ_APIKEY_PRIVATE[0]
        mailjet = Client(auth=(api_key, api_secret), version='v3.1')
        return mailjet.send.create(data=data)

    @staticmethod
    def _get_mailjet_variables(suggestions, first_name, problem):
        """
        You might be wondering why we don't just use the PracticeSerializer and handle
        the display in Mailjet's templating language. The reason is that MJ is full of bugs
        like being unable to access object properties, errors when a variable is null, etc.
        The only way of sending the email is to have a one-level plain object with no arrays
        nor null values.
        """
        variables = {}
        variables['first_name'] = first_name or ''
        variables['problem'] = (problem or '').lower()

        for i in range(min(len(suggestions), 3)):
            practice = suggestions[i]
            position = str(i + 1)
            variables['mechanism_' + position] = (practice.mechanism.name or '') if practice.mechanism else ''
            variables['mechanism_description_' + position] = (practice.mechanism.description or '') if practice.mechanism else ''
            variables['equipment_' + position] = practice.equipment or ''
            variables['additional_benefits_' + position] = practice.additional_benefits or ''
            variables['success_factors_' + position] = practice.success_factors or ''
            variables['impact_' + position] = practice.impact or ''
            variables['schedule_' + position] = practice.schedule or ''
            variables['title_' + position] = practice.title or ''
            variables['description_' + position] = practice.description or ''
            variables['cta_label_' + position] = (practice.main_resource_label or '') if practice.main_resource_label else ''
            variables['cta_url_' + position] = (practice.main_resource.url or '') if practice.main_resource else ''

            resource_labels = []
            links_html = ''
            type_label = {
                1: 'le site web',
                2: 'le document',
                3: 'la vidéo',
            }

            for resource in list(practice.secondary_resources.all()):
                resource_type = type_label[resource.resource_type] if resource.resource_type in type_label.keys() else 'la resource'
                resource_labels.append("{0} <a href='{1}'>{2}</a>".format(resource_type, (resource.url or ''), (resource.name or '')))

            start = 'Pour plus d\'informations voici'
            if len(resource_labels) == 1:
                links_html = '{0} {1}'.format(start, resource_labels[0])
            if len(resource_labels) > 1:
                links_html = '{0} {1} et {2}'.format(start, ', '.join(resource_labels[:-1]), resource_labels[-1])

            variables['html_text_' + position] = links_html

        return variables


class SendTaskView(APIView):
    """
    This view will send a task to Asana in order to follow-up the
    implementation of a certain practice.
    """
    authentication_classes = [authentication.SessionAuthentication]
    permission_classes = [permissions.IsAuthenticated | HasAPIKey]

    def post(self, request):
        name = request.data.get('name')
        email = request.data.get('email')
        phone_number = request.data.get('phone_number')
        practice_id = request.data.get('practice_id')
        answers = request.data.get('answers')
        problem = request.data.get('problem') or request.data.get('reason')
        date = request.data.get('datetime')

        # We need at least name and phone number
        if not name or not phone_number:
            return JsonResponse({'error': 'Missing information'}, status=400)

        # If we have a date, it needs to be a valid one
        if date:
            try:
                date = dateutil.parser.parse(date)
            except ValueError as _:
                return JsonResponse({'error': 'Invalid date'}, status=400)

        notes = '{0}\n\n'.format(problem or '')

        if practice_id:
            practice_url = 'https://airtable.com/tblobpdQDxkzcllWo/{0}'.format(practice_id)
            notes += '{0} a besoin d\'aide pour implémenter la pratique {1}.\n\n'.format(name, practice_url)
        else:
            notes += '{0} a partagé son information de contact.\n\n'.format(name)

        notes += 'Num tel : {0}\n\n'.format(phone_number)

        if email:
            notes += 'Email: {0}\n\n'.format(email)

        if answers:
            notes += 'Réponses :\n{0}'.format(answers)

        try:
            SendTaskView._send_task(settings.ASANA_PROJECT, name, notes, date)
            return JsonResponse({}, status=200)
        except asana.error.InvalidRequestError as _:
            return JsonResponse({'error': 'Invalid request'}, status=400)
        except asana.error.InvalidTokenError as _:
            return JsonResponse({'error': 'Invalid token'}, status=403)
        return JsonResponse({'error': 'Invalid request'}, status=400)

    @staticmethod
    def _send_task(projects, name, notes, due_at):
        client = asana.Client.access_token(settings.ASANA_PERSONAL_TOKEN)
        date = due_at.astimezone().isoformat() if due_at else None
        # pylint: disable=no-member
        client.tasks.create({
            'projects': projects,
            'due_at': date,
            'name': name,
            'notes': notes,
        })
        # pylint: enable=no-member


class StatsView(APIView):
    """
    Temporary view that will increment the counters of stat models
    such as groupCount.
    """

    def post(self, request):
        groups = request.data.get('groups')
        referers = request.data.get('referers')

        try:
            StatsView._increment_groups(groups)
            StatsView._increment_referers(referers)
            return JsonResponse({}, status=200)
        except Exception as _:
            return JsonResponse({}, status=400)

    @staticmethod
    def _increment_groups(groups):
        for group in groups.split(','):
            GroupCount.create_or_increment(GroupCount.AgriculturalGroup[group])

    @staticmethod
    def _increment_referers(referers):
        for referer in referers.split(','):
            RefererCount.create_or_increment(RefererCount.Referer[referer])


class DiscardActionView(CreateAPIView):
    serializer_class = DiscardActionSerializer

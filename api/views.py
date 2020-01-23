import dateutil.parser
from itertools import chain
from django.http import HttpResponse, JsonResponse
from django.conf import settings
from rest_framework.renderers import JSONRenderer
from rest_framework.views import APIView
from rest_framework.generics import CreateAPIView, ListAPIView
from rest_framework import permissions, authentication
from rest_framework_api_key.permissions import HasAPIKey
import asana
from data.adapters import AirtableAdapter
from data.models import GroupCount, RefererCount, Category
from api.engine import Engine
from api.serializers import ResponseSerializer, DiscardActionSerializer, CategorySerializer
from api.formschema import get_form_schema
from api.models import Response


class RankingsApiView(APIView):
    """
    This view will return a list of practice IDs that
    correspond to the form from FormView.
    """

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

    def get(self, request):
        return JsonResponse(get_form_schema())


class SendTaskView(APIView):
    """
    This view will send a task to Asana in order to follow-up the
    implementation of a certain practice.
    """
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
        groups = groups if isinstance(groups, list) else groups.split(',')
        for group in groups:
            GroupCount.create_or_increment(GroupCount.AgriculturalGroup[group])

    @staticmethod
    def _increment_referers(referers):
        referers = referers if isinstance(referers, list) else referers.split(',')
        for referer in referers:
            RefererCount.create_or_increment(RefererCount.Referer[referer])


class CategoriesView(ListAPIView):
    queryset = Category.objects
    serializer_class = CategorySerializer


class DiscardActionView(CreateAPIView):
    serializer_class = DiscardActionSerializer

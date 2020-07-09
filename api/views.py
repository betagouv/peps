import dateutil.parser
import asana
from django.http import HttpResponse, JsonResponse
from django.conf import settings
from django.contrib.auth.models import User
from django.views.decorators.cache import cache_control
from rest_framework.renderers import JSONRenderer
from rest_framework.views import APIView
from rest_framework.generics import CreateAPIView, ListAPIView, RetrieveAPIView
from rest_framework.generics import UpdateAPIView, ListCreateAPIView
from rest_framework import permissions, authentication
from data.adapters import PracticesAirtableAdapter
from data.models import Category, Farmer, Experiment, Message
from api.engine import Engine
from api.serializers import ResponseSerializer, DiscardActionSerializer, CategorySerializer
from api.serializers import FarmerSerializer, UserSerializer, ExperimentSerializer
from api.serializers import MessageSerializer
from api.formschema import get_form_schema
from api.geojson import get_geojson
from api.models import Response
from api.permissions import IsExperimentAuthor, IsFarmer, IsProfileOwner
from api.utils import AsanaUtils

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
    This view will refresh the DB for practice data
    """
    authentication_classes = [authentication.SessionAuthentication]
    permission_classes = [permissions.IsAdminUser]

    def post(self, request):
        errors = PracticesAirtableAdapter.update()
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

class GeojsonView(APIView):
    """
    This view will return the geojson with France's departments
    """

    @cache_control(max_age=31536000)
    def get(self, request):
        return JsonResponse(get_geojson())


class SendTaskView(APIView):
    """
    This view will send a task to Asana in order to follow-up the
    implementation of a certain practice.
    """
    def post(self, request):
        task_name = request.data.get('name')
        email = request.data.get('email')
        phone_number = request.data.get('phone_number')
        practice_id = request.data.get('practice_id')
        answers = request.data.get('answers')
        problem = request.data.get('problem') or request.data.get('reason')
        date = request.data.get('datetime')

        # We need at least name and phone number
        if not task_name or not phone_number:
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
            notes += '{0} a besoin d\'aide pour implémenter la pratique {1}.\n\n'.format(task_name, practice_url)
        else:
            notes += '{0} a partagé son information de contact.\n\n'.format(task_name)

        notes += 'Num tel : {0}\n\n'.format(phone_number)

        if email:
            notes += 'Email: {0}\n\n'.format(email)

        if answers:
            notes += 'Réponses :\n{0}'.format(answers)

        try:
            AsanaUtils.send_task(settings.ASANA_PROJECT, task_name, notes, date)
            return JsonResponse({}, status=200)
        except asana.error.InvalidRequestError as _:
            return JsonResponse({'error': 'Invalid request'}, status=400)
        except asana.error.InvalidTokenError as _:
            return JsonResponse({'error': 'Invalid token'}, status=403)
        return JsonResponse({'error': 'Invalid request'}, status=400)


class CategoriesView(ListAPIView):
    queryset = Category.objects
    serializer_class = CategorySerializer


class DiscardActionView(CreateAPIView):
    serializer_class = DiscardActionSerializer


class FarmersView(ListAPIView):
    queryset = Farmer.objects.filter(approved=True)
    serializer_class = FarmerSerializer

    def get_queryset(self):
        """
        We will return approved farmers as well as the one corresponding
        to the logged user (even if it is not yet approved)
        """
        user = self.request.user
        approved_farmers = Farmer.objects.filter(approved=True)
        if hasattr(user, 'farmer') and user.farmer:
            return approved_farmers | Farmer.objects.filter(id=user.farmer.id)
        return approved_farmers

class ExperimentView(UpdateAPIView):
    permission_classes = [permissions.IsAuthenticated & IsFarmer & IsExperimentAuthor]
    serializer_class = ExperimentSerializer
    queryset = Experiment.objects

    def put(self, request, *args, **kwargs):
        return JsonResponse({'error': 'Only PATCH request supported in this resource'}, status=405)

    def patch(self, request, *args, **kwargs):
        return self.partial_update(request, *args, **kwargs)


class ExperimentCreateView(CreateAPIView):
    permission_classes = [permissions.IsAuthenticated & IsFarmer]
    serializer_class = ExperimentSerializer

    def perform_create(self, serializer):
        farmer = self.request.user.farmer
        try:
            task_name = 'Nouvelle XP créée par ' + str(farmer.name) + ' en attente de validation'
            notes = 'Une nouvelle XP est en attente de validation.'
            AsanaUtils.send_task(settings.ASANA_PROJECT, task_name, notes, None)
        finally:
            serializer.save(farmer=farmer)


class LoggedUserView(RetrieveAPIView):
    model = User
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]
    queryset = User.objects.all()

    def get_object(self):
        return self.request.user


class FarmerView(UpdateAPIView):
    permission_classes = [permissions.IsAuthenticated & IsFarmer & IsProfileOwner]
    serializer_class = FarmerSerializer
    queryset = Farmer.objects

    def put(self, request, *args, **kwargs):
        return JsonResponse({'error': 'Only PATCH request supported in this resource'}, status=405)

    def patch(self, request, *args, **kwargs):
        return self.partial_update(request, *args, **kwargs)

class UpdateMessageView(UpdateAPIView):
    permission_classes = [permissions.IsAuthenticated & IsFarmer]
    serializer_class = MessageSerializer

    def get_queryset(self):
        farmer = self.request.user.farmer
        return Message.objects.filter(recipient=farmer) | Message.objects.filter(sender=farmer)

class ListCreateMessageView(ListCreateAPIView):
    permission_classes = [permissions.IsAuthenticated & IsFarmer]
    serializer_class = MessageSerializer

    def get_queryset(self):
        farmer = self.request.user.farmer
        return Message.objects.filter(recipient=farmer) | Message.objects.filter(sender=farmer)


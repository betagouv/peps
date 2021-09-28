import os
import dateutil.parser
import asana
from django.http import HttpResponse, JsonResponse
from django.template import loader
from django.core.mail import EmailMultiAlternatives
from django.conf import settings
from django.contrib.auth import get_user_model
from django.views.decorators.cache import cache_control
from django.utils import timezone
from rest_framework.renderers import JSONRenderer
from rest_framework.views import APIView
from rest_framework.generics import CreateAPIView, ListAPIView, RetrieveAPIView
from rest_framework.generics import UpdateAPIView, ListCreateAPIView
from rest_framework.exceptions import ValidationError
from rest_framework import permissions, authentication, status
from data.models import Farmer, Experiment, Message, Theme
from api.serializers import FarmerSerializer, LoggedUserSerializer, ExperimentSerializer
from api.serializers import MessageSerializer, FarmerFastSerializer, ExperimentBriefsFastSerializer
from api.serializers import FarmerBriefsFastSerializer, ThemeFastSerializer
from api.geojson import get_geojson
from api.permissions import IsExperimentAuthor, IsFarmer, IsProfileOwner
from api.utils import AsanaUtils


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
        except Exception as e:
            return JsonResponse({'error': 'Server error'}, status=500)


class FarmersView(ListAPIView):
    serializer_class = FarmerFastSerializer

    def get_queryset(self):
        """
        We will return approved farmers as well as the one corresponding
        to the logged user (even if it is not yet approved)
        """
        user = self.request.user
        queryset = Farmer.objects.filter(approved=True)
        if hasattr(user, 'farmer') and user.farmer:
            queryset = queryset | Farmer.objects.filter(id=user.farmer.id)
        return queryset.prefetch_related('images', 'experiments', 'experiments__images', 'experiments__videos')


class FarmersRetrieveView(RetrieveAPIView):
    model = Farmer
    serializer_class = FarmerFastSerializer
    queryset = Farmer.objects.filter(approved=True)
    lookup_field = 'sequence_number'

    def get_queryset(self):
        user = self.request.user
        queryset = Farmer.objects.filter(approved=True)
        if hasattr(user, 'farmer') and user.farmer:
            queryset = queryset | Farmer.objects.filter(id=user.farmer.id)
        return queryset.prefetch_related('images', 'experiments', 'experiments__images', 'experiments__videos')


class FarmerBriefsListView(ListAPIView):
    serializer_class = FarmerBriefsFastSerializer

    def get_queryset(self):
        """
        We will return approved experiments in a short format only
        """
        queryset = Farmer.objects.filter(approved=True)
        return queryset

class ExperimentBriefsListView(ListAPIView):
    serializer_class = ExperimentBriefsFastSerializer

    def get_queryset(self):
        """
        We will return approved experiments in a short format only
        """
        queryset = Experiment.objects.filter(state="Validé")
        return queryset.prefetch_related('images', 'farmer')

class ThemeListView(ListAPIView):
    serializer_class = ThemeFastSerializer
    queryset = Theme.objects.filter(active=True)

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
        except Exception as _:
            pass
        finally:
            serializer.save(farmer=farmer)


class LoggedUserView(RetrieveAPIView):
    model = get_user_model()
    serializer_class = LoggedUserSerializer
    permission_classes = [permissions.IsAuthenticated]
    queryset = get_user_model().objects.all()

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

class ListCreateMessageView(ListCreateAPIView):
    permission_classes = [permissions.IsAuthenticated & IsFarmer]
    serializer_class = MessageSerializer

    def get_queryset(self):
        farmer = self.request.user.farmer
        queryset = Message.objects.filter(recipient=farmer, pending_delivery=False) | Message.objects.filter(sender=farmer)
        if self.request.method == "GET" and self.request.GET.get('since'):
            try:
                date_string = self.request.GET.get('since')
                date = dateutil.parser.isoparse(date_string)
                queryset = queryset & Message.objects.filter(sent_at__gte=date)
            except Exception as _:
                raise ValidationError('Invalid date querystring parameter')
        return queryset.prefetch_related('recipient', 'sender')

    def perform_create(self, serializer):
        farmer = self.request.user.farmer
        can_send_messages = farmer.can_send_messages
        serializer.save(pending_delivery=not can_send_messages)
        try:
            if can_send_messages:
                self.send_email()
            else:
                task_name = 'Message de ' + str(farmer.name) + ' en attente de validation'
                notes = str(farmer.name) + "a tenté d'envoyer un message, mais il n'est pas encore authorisé."
                AsanaUtils.send_task(settings.ASANA_PROJECT, task_name, notes, None)
        except Exception as _:
            pass

    def send_email(self):
        recipient_id = self.request.data.get('recipient')
        recipient_farmer = Farmer.objects.get(pk=recipient_id)

        if not recipient_farmer.email_for_messages_allowed:
            return

        protocol = 'https://' if os.getenv('PEPS_SECURE') == 'True' else 'http://'
        domain = protocol + os.getenv('PEPS_HOSTNAME', '')

        sender_farmer = self.request.user.farmer
        email_address = recipient_farmer.user.email
        email_subject = "Nouveau message de {0} sur Peps".format(sender_farmer.name)
        html_template = 'email-message.html'
        text_template = 'email-message.txt'
        context = {
            'recipient_name': recipient_farmer.name,
            'sender_name': sender_farmer.name,
            'body': self.request.data.get('body'),
            'link': '/login?next=/messages',
            'domain': domain,
        }
        text_message = loader.render_to_string(text_template, context)
        html_message = loader.render_to_string(html_template, context)
        email = EmailMultiAlternatives(
            email_subject,
            text_message,
            settings.DEFAULT_FROM_EMAIL,
            [email_address],
            headers={}
        )
        email.attach_alternative(html_message, 'text/html')
        email.send()

class MarkAsReadMessageView(APIView):
    permission_classes = [permissions.IsAuthenticated & IsFarmer]

    def post(self, request):
        message_ids = request.data
        if not isinstance(message_ids, list):
            return JsonResponse('The request must contain an array of IDs', status.HTTP_400_BAD_REQUEST)

        message_queryset = (Message
                            .objects
                            .filter(pk__in=message_ids, recipient=request.user.farmer, read_at__isnull=True))
        modified_messages_id = list(message_queryset.values_list('id', flat=True))
        message_queryset.update(read_at=timezone.now())

        response_data = JSONRenderer().render(MessageSerializer(Message.objects.filter(pk__in=modified_messages_id), many=True).data)
        return HttpResponse(response_data, content_type="application/json")

class StatsView(APIView):
    """
    This view will return statistics on Peps
    """

    def get(self, request):
        distinct_messages = Message.objects.values('recipient', 'sender').distinct()
        existing_correspondance = set()

        for message in distinct_messages:
            key = ''.join(sorted([str(message['sender']), str(message['recipient'])]))
            existing_correspondance.add(key)

        return JsonResponse({
            "approvedExperimentCount": Experiment.objects.filter(state='Validé').count(),
            "approvedFarmerCount": Farmer.objects.filter(approved=True).count(),
            "contactCount": len(existing_correspondance),
        })

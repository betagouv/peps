from django.conf.urls import url
from django.urls import path
from rest_framework.urlpatterns import format_suffix_patterns
from api.views import RankingsApiView, RefreshDataApiView, FormSchemaView, GeojsonView
from api.views import SendTaskView, DiscardActionView, CategoriesView
from api.views import FarmersView, LoggedUserView, ExperimentView, FarmerView
from api.views import ExperimentCreateView, ListCreateMessageView
from api.views import MarkAsReadMessageView, StatsView, ExperimentBriefsListView
from api.views import FarmersRetrieveView, FarmerBriefsListView, ThemeListView

urlpatterns = {
    url(r'^calculateRankings/?$', RankingsApiView.as_view(), name='calculate_rankings'),
    url(r'^refreshData/?$', RefreshDataApiView.as_view(), name='refresh_data'),
    url(r'^formSchema/?$', FormSchemaView.as_view(), name='form_schema'),
    url(r'^sendTask/?$', SendTaskView.as_view(), name='send_task'),
    url(r'^discardAction/?$', DiscardActionView.as_view(), name='discard_action'),
    url(r'^categories/?$', CategoriesView.as_view(), name='get_categories'),
    url(r'^farmers/?$', FarmersView.as_view(), name='get_farmers'),
    url(r'^farmerBriefs/?$', FarmerBriefsListView.as_view(), name='get_farmer_briefs'),
    path('farmers/<int:sequence_number>', FarmersRetrieveView.as_view(), name='get_farmer'),
    url(r'^loggedUser/?$', LoggedUserView.as_view(), name='logged_user'),
    url(r'^experiments/?$', ExperimentCreateView.as_view(), name='experiment_create'),
    url(r'^experimentBriefs/?$', ExperimentBriefsListView.as_view(), name='get_xp_briefs'),
    path('experiments/<uuid:pk>', ExperimentView.as_view(), name='experiment_update'),
    path('farmers/<uuid:pk>', FarmerView.as_view(), name='farmer_update'),
    url(r'^geojson/?$', GeojsonView.as_view(), name='geojson'),
    url(r'^stats/?$', StatsView.as_view(), name='stats'),
    url(r'^themes/?$', ThemeListView.as_view(), name='get_themes'),

    url(r'^messages/?$', ListCreateMessageView.as_view(), name='messages'),
    path('messages/markAsRead', MarkAsReadMessageView.as_view(), name='mark_as_read'),
}

urlpatterns = format_suffix_patterns(urlpatterns)

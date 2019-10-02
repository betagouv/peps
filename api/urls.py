from django.conf.urls import url
from rest_framework.urlpatterns import format_suffix_patterns
from api.views import RankingsApiView, RefreshDataApiView, FormSchemaView, SendEmailView

urlpatterns = {
    url(r'^calculateRankings/?$', RankingsApiView.as_view(), name='calculate_rankings'),
    url(r'^refreshData/?$', RefreshDataApiView.as_view(), name='refresh_data'),
    url(r'^formSchema/?$', FormSchemaView.as_view(), name='form_schema'),
    url(r'^sendEmail/?$', SendEmailView.as_view(), name='send_email'),
}

urlpatterns = format_suffix_patterns(urlpatterns)

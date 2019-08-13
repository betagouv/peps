from django.conf.urls import url
from rest_framework.urlpatterns import format_suffix_patterns
from api.views import RankingsApiView, RefreshDataApiView, FormSchemaView

urlpatterns = {
    url(r'^calculateRankings/?$', RankingsApiView.as_view(), name='calculate_rankings'),
    url(r'^refreshData/?$', RefreshDataApiView.as_view(), name='refresh_data'),
    url(r'^formSchema/?$', FormSchemaView.as_view(), name='form_schema')
}

urlpatterns = format_suffix_patterns(urlpatterns)

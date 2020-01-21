from django.conf.urls import url
from rest_framework.urlpatterns import format_suffix_patterns
from api.views import RankingsApiView, RefreshDataApiView, FormSchemaView
from api.views import SendTaskView, DiscardActionView, StatsView, CategoriesView

urlpatterns = {
    url(r'^calculateRankings/?$', RankingsApiView.as_view(), name='calculate_rankings'),
    url(r'^refreshData/?$', RefreshDataApiView.as_view(), name='refresh_data'),
    url(r'^formSchema/?$', FormSchemaView.as_view(), name='form_schema'),
    url(r'^sendTask/?$', SendTaskView.as_view(), name='send_task'),
    url(r'^discardAction/?$', DiscardActionView.as_view(), name='discard_action'),
    url(r'^stats/?$', StatsView.as_view(), name='register_stats'),
    url(r'^categories/?$', CategoriesView.as_view(), name='register_categories'),
}

urlpatterns = format_suffix_patterns(urlpatterns)

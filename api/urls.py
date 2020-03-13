from django.conf.urls import url
from rest_framework.urlpatterns import format_suffix_patterns
from api.views import RankingsApiView, RefreshDataApiView, FormSchemaView
from api.views import SendTaskView, DiscardActionView, StatsView, CategoriesView
from api.views import RefreshXPDataApiView, FarmersView, ExperimentsView

urlpatterns = {
    url(r'^calculateRankings/?$', RankingsApiView.as_view(), name='calculate_rankings'),
    url(r'^refreshData/?$', RefreshDataApiView.as_view(), name='refresh_data'),
    url(r'^refreshXPData/?$', RefreshXPDataApiView.as_view(), name='refresh_xp_data'),
    url(r'^formSchema/?$', FormSchemaView.as_view(), name='form_schema'),
    url(r'^sendTask/?$', SendTaskView.as_view(), name='send_task'),
    url(r'^discardAction/?$', DiscardActionView.as_view(), name='discard_action'),
    url(r'^stats/?$', StatsView.as_view(), name='register_stats'),
    url(r'^categories/?$', CategoriesView.as_view(), name='get_categories'),
    url(r'^farmers/?$', FarmersView.as_view(), name='get_farmers'),
    url(r'^experiments/?$', ExperimentsView.as_view(), name='get_experiments'),
}

urlpatterns = format_suffix_patterns(urlpatterns)

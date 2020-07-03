from django.urls import path
from django.views.generic.base import RedirectView
from django.views.decorators.cache import cache_page
from django.contrib.sitemaps.views import sitemap
from web.views import SimulatorFormView, VueAppDisplayView, logout_view, RegisterView
from web.sitemaps import FarmerSitemap, ExperimentSitemap, WebSitemap

sitemaps = {
    'farmers': FarmerSitemap,
    'experiments': ExperimentSitemap,
    'other': WebSitemap,
}

urlpatterns = [
    path('', VueAppDisplayView.as_view(), name='app'),
    path('app/', RedirectView.as_view(pattern_name="app"), name='app_redirect'),
    path('simulator', SimulatorFormView.as_view(), name='form_view'),
    path('logout', logout_view, name='logout'),
    path('register', RegisterView.as_view(), name='register'),
    path('sitemap.xml', cache_page(60*60)(sitemap), {'sitemaps': sitemaps}, name="sitemap")
]

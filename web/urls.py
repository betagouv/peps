from django.urls import path
from web.views import FormView, VueAppDisplayView, logout_view

urlpatterns = [
    path('', VueAppDisplayView.as_view(), name='app'),
    path('simulator', FormView.as_view(), name='form_view'),
    path('logout', logout_view, name='logout'),
]

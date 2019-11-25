from django.urls import path
from django.contrib.auth import views as auth_views
from django.views.generic import TemplateView
from web.views import FormView, UserDisplayView, AppDisplayView, VueAppDisplayView

urlpatterns = [
    path('', AppDisplayView.as_view(), name='app'),
    path('simulator', FormView.as_view(), name='form_view'),
    path('vueapp', VueAppDisplayView.as_view(), name='vueapp'),
    path('userDisplay', UserDisplayView.as_view(), name='user_display'),
    path('accounts/login/', auth_views.LoginView.as_view(), name='login'),
]

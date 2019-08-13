from django.urls import path
from django.contrib.auth import views as auth_views
from web.views import FormView, UserDisplayView, ProductionSystemFormView

urlpatterns = [
    path('', FormView.as_view(), name='form_view'),
    path('productionSystemForm', ProductionSystemFormView.as_view(), name='form_redirect'),
    path('userDisplay', UserDisplayView.as_view(), name='user_display'),
    path('accounts/login/', auth_views.LoginView.as_view(), name='login'),
]

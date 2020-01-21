from django.conf.urls import url, include
from django.conf import settings
from django.urls import path
from django.contrib import admin
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls)
]

urlpatterns.append(url(r'', include('web.urls')))
urlpatterns.append(url(r'^api/v1/', include('api.urls')))

if settings.DEBUG:
    urlpatterns += staticfiles_urlpatterns()
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

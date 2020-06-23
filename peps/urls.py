from django.conf.urls import url, include
from django.conf import settings
from django.urls import path
from django.contrib import admin
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.conf.urls.static import static
from magicauth.urls import urlpatterns as magicauth_urls
from web.views import VueAppDisplayView

urlpatterns = [
    path('admin/', admin.site.urls)
]

urlpatterns.append(url(r'', include('web.urls')))
urlpatterns.append(url(r'^api/v1/', include('api.urls')))

urlpatterns.extend(magicauth_urls)

if settings.DEBUG:
    urlpatterns += staticfiles_urlpatterns()
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

# In order for vue-history to work in HTML5 mode, we need to add a catch-all
# route returning the app (https://router.vuejs.org/guide/essentials/history-mode.html#html5-history-mode)
urlpatterns.append(url(r'^.*/$', VueAppDisplayView.as_view()))

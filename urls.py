# coding=utf-8

from django.conf import settings
from django.conf.urls import url, include
from django.conf.urls.static import static
from django.contrib import admin

admin.autodiscover()

urlpatterns = [
    url(r'^admin/', include(admin.site.urls)),

    url(r'^docs/', include('rest_framework_swagger.urls')),

    url(r'^api/', include('api.urls', namespace='api')),
] + static(settings.STATIC_URL, document=settings.STATIC_ROOT)

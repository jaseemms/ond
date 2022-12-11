from django.conf.urls import url, include
from django.contrib import admin
from django.conf import settings
from django.views.static import serve
from django.contrib.auth import views as auth_views

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^', include('django.contrib.auth.urls')),
    
    url(r'^', include('ads.urls',namespace='ads')),
    url(r'^', include('users.urls',namespace='users')),

    url(r'^static/(?P<path>.*)$', serve, { 'document_root': settings.STATIC_FILE_ROOT,}),
    url(r'^media/(?P<path>.*)$', serve, { 'document_root': settings.MEDIA_ROOT,}),
]

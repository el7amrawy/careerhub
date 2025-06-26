"""project URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import include, path
from django.conf import settings
from django.conf.urls.static import static
from job import views as job_views
from django.views.generic import RedirectView
from django.views.static import serve
from django.conf.urls import url
from . import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('home.urls', namespace='home')),
    path('jobs/', include('job.urls', namespace='jobs')),
    path('accounts/', include('accounts.urls', namespace='accounts')),
    path('contact/', include('contact.urls', namespace='contact')),
    path('chatbot/ask/', views.chatbot_ask, name='chatbot_ask'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

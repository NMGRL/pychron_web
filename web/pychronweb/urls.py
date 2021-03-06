"""pychronweb URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf.urls import url
from django.contrib import admin
from django.urls import path, include

from pychronweb import views
from samples.views import ProjectAutocomplete, PrincipalInvestigatorAutocomplete, \
    SampleAutocomplete

urlpatterns = [
    path('', views.index, name='home'),
    path('stats/', include('stats.urls')),
    path('admin/', admin.site.urls),
    path('samples/', include('samples.urls')),
    path('projects/', include('projects.urls')),
    path('materials/', include('materials.urls')),
    path('events/', include('events.urls')),
    path('analyses/', include('analyses.urls')),
    path('principal_investigators/', include('principal_investigators.urls')),
    path('packages/', include('packages.urls')),
    path('accounts/', include('django.contrib.auth.urls')),

    url(r"^", include("users.urls")),

    path('project-autocomplete/', ProjectAutocomplete.as_view(), name='project-autocomplete'),
    path('sample-autocomplete/', SampleAutocomplete.as_view(), name='sample-autocomplete'),
    # path('material-autocomplete/', MaterialAutocomplete.as_view(), name='material-autocomplete'),
    path('principalinvestigator-autocomplete/', PrincipalInvestigatorAutocomplete.as_view(),
         name='principalinvestigator-autocomplete')

]

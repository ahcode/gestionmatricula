"""Matricula URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.10/topics/http/urls/
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
from django.conf.urls import url, include
from django.contrib import admin
from django.conf.urls.static import static
from django.conf import settings
from usuarios import views as usuarios_views
from django.contrib.auth import views as auth_views
from django.core.urlresolvers import reverse_lazy

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^registro/(alumno|profesor)/$', usuarios_views.registro, name='registro'),
    url(r'^login/$', auth_views.login, {'template_name': 'usuarios/login.html'}, name='login'),
    url(r'^logout/$', auth_views.logout, {'next_page': reverse_lazy('gestion:index')}, name='logout'),
    url(r'^', include('gestion.urls', namespace='gestion'), name='gestion'),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

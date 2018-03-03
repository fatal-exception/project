"""samtla_com URL Configuration

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
from django.conf.urls import url
from django.contrib import admin
from samtla import views


urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^$', views.signin, name='login'),
    url(r'^logout$', views.signout, name='logout'),
    url(r'^register$', views.register, name='register'),
    url(r'^authenticate$', views.authenticate, name='authenticate'),
    url(r'^home$', views.home, name='home'),
    url(r'^select$', views.select, name='home'),
    url(r'^browse$', views.Browse, name='browse'),
    url(r'^search$', views.Search, name='search'),
    url(r'^relatedqueries$', views.RelatedQueries, name='relatedqueries'),
    url(r'^document$', views.Document, name='document'),
    url(r'^document_related$', views.RelatedDocuments, name='relateddocuments'),
    url(r'^document_original$', views.Original, name='document_original'),
    url(r'^document_title$', views.DocumentTitle, name='document_title'),
    url(r'^document_compare$', views.Compare, name='compare'),
    url(r'^document_metadata$', views.DocumentMetadata, name='metadata'),
    url(r'^NER$', views.NER, name='NER'),
    url(r'^KML$', views.KML, name='KML'),

]

from django.conf.urls import patterns, url

from itfornonprofits import views

urlpatterns = patterns('',
    url(r'^$', views.index, name='index'),
    url(r'^$', views.index, name='addproject'),
    url(r'^$', views.index, name='viewprojects')
)
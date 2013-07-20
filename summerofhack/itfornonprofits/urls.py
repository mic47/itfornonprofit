from django.conf.urls import patterns, url

from itfornonprofits import views

urlpatterns = patterns('',
    url(r'^$', views.index, name='index'),
    url(r'^addproject$', views.addproject, name='addproject'),
    url(r'^viewprojects$', views.viewprojects, name='viewprojects')
)

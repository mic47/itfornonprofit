from django.conf.urls import patterns, url

from itfornonprofits import views

urlpatterns = patterns('',
    url(r'^$', views.index, name='index'),
    url(r'^addproject$', views.addproject, name='addproject'),
    url(r'^createprojectindb$', views.createprojectindb, name='createprojectindb'),
    url(r'^viewprojects$', views.viewprojects, name='viewprojects'),
    url(r'^viewproject/(\d)$', views.viewproject, name='viewproject'),
    url(r'^contactproject$', views.contactproject, name='contactproject'),
    url(r'^viewengineers$', views.viewengineers, name='viewengineers'),
    url(r'^registerengineer$', views.registerengineer, name='registerengineer'),
    url(r'^createengineer$', views.createengineer, name='createengineer'),
    url(r'^addskilltoproject/(\d)$', views.addskilltoproject, name='addskilltoproject'),
    url(r'^backproject/([0-9XY]*)/([0-9XY]*)$', views.backproject, name='backproject'),
    url(r'^finishproject/(\d)$', views.finishproject, name='finishproject'),
)

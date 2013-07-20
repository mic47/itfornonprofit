from django.shortcuts import render

from itfornonprofits.models import Project

def index(request):
    num_projects = len(Project.objects.all())
    context = {'num_projects': num_projects}
    return render(request, 'itfornonprofits/index.html', context)

def addproject():
	pass

def viewprojects():
	pass
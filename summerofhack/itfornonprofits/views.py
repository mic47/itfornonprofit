from django.shortcuts import render
from django.http import HttpResponse

from itfornonprofits.models import Project

def index(request):
    num_projects = len(Project.objects.all())
    context = {'num_projects': num_projects}
    return render(request, 'itfornonprofits/index.html', context)

def addproject(request):
   # f = ProjectForm(request.POST)
   # new_project = f.save()
    return render(request, 'itfornonprofits/addproject.html')

def viewprojects(request):
	return HttpResponse("Hello world")
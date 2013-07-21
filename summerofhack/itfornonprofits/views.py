from django.shortcuts import render
from django.http import HttpResponse
import json
import datetime
from itfornonprofits.models import Project
from itfornonprofits.models import Sector
from itfornonprofits.models import Skill

def index(request):
    num_projects = len(Project.objects.all())
    context = {'num_projects': num_projects}
    return render(request, 'itfornonprofits/index.html', context)

def idx(d, v, default=None):
    if v in d:
        return d[v]
    return default

def addproject(request):
    return render(request, 'itfornonprofits/addproject.html')

def createprojectindb(request):
    p = Project(name=request.POST['name'], description=request.POST['description'], time_needed=request.POST['time_needed'], date_created=datetime.datetime.now())
    p.save()
    sectors = [x.strip() for x in str(idx(request.POST, 'sectors', '')).split(',')]
    for sector in sectors:
    	project_sector = Sector.objects.filter(name=sector)
    	if (len(project_sector) == 0):
    		project_sector = Sector()
    		project_sector.name = sector
    		project_sector.save()
    	else:
    		project_sector = project_sector[0]
    	p.sectors.add(project_sector)
    skills = [x.strip() for x in str(idx(request.POST, 'skills', '')).split(',')]
    for skill in skills:
    	project_skill = Skill.objects.filter(name=skill)
    	if (len(project_skill) == 0):
    		project_skill = Skill()
    		project_skill.name = skill
    		project_skill.save()
    	else:
    		project_skill = project_skill[0]
    	p.skills.add(project_skill)

    return render(request, 'itfornonprofits/viewprojects.html')

def filter_list(wat, stuff):
    intersection = set(wat).intersection(set(stuff)) 
    return len(intersection) > 0 or len(wat) == 0

def viewprojects(request):
    # Keyword search
    # Match na aspon jeden skill, aspon jeden vector
    objects = Project.objects
    maxtime = int(idx(request.POST, 'maxtime', '0'))
    mintime = int(idx(request.POST, 'mintime', '0'))
    keyword = str(idx(request.POST, 'keyword', ''))
    print request.POST
    print 'keyword' in request.POST
    print idx(request.POST, 'keyword', '')
    sectors = [x.strip() for x in str(idx(request.POST, 'sectors', '')).split(',')]
    skills = [x.strip() for x in str(idx(request.POST, 'skills', '')).split(',')]
    print sectors
    print skills
    if sectors == ['']:
        sectors = []
    if skills == ['']:
        skills = []
    if maxtime > 0:
        objects = objects.filter(time_needed__lte=maxtime)
    if mintime > 0:
        objects = objects.filter(time_needed__gte=mintime)
    print keyword
    if len(keyword) > 0:
        objects = objects.filter(description__contains=keyword)
    if type(objects != list):
        objects = objects.all()
    if len(skills) > 0:
        objects = filter(lambda x: filter_list([y.name for y in x.skills.all()], skills), objects)
    if len(sectors) > 0:
        objects = filter(lambda x: filter_list([y.name for y in x.sectors.all()], sectors), objects)
    projects = objects
    new_projects = []
    for project in projects:
        project.new_skills =  ', '.join([str(s.name) for s in project.skills.all()])
        project.new_sectors = ', '.join([str(s.name) for s in project.sectors.all()])
        new_projects.append(project)
    sectors_list = json.dumps(sorted([sector.name for sector in Sector.objects.all()]))
    skills_list = json.dumps(sorted([skill.name for skill in Skill.objects.all()]))
    print sectors_list
    context = {'projects': new_projects, 'sectors_list': sectors_list, 'skills_list': skills_list}
    return render(request, 'itfornonprofits/viewprojects.html', context)

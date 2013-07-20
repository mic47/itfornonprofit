from django.shortcuts import render

from itfornonprofits.models import Project

def index(request):
    num_projects = len(Project.objects.all())
    context = {'num_projects': num_projects}
    return render(request, 'itfornonprofits/index.html', context)

def addproject():
    pass

def idx(d, v, default=None):
    if v in d:
        return d[v]
    return default

def filter_list(wat, stuff):
    intersection = set(wat).intersection(set(stuff)) 
    return len(intersection) > 0

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
    context = {'projects': new_projects}
    return render(request, 'itfornonprofits/viewprojects.html', context)

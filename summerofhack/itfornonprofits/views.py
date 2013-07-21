from django.shortcuts import render
from django.http import HttpResponse
import json
import datetime
import email
import smtplib
from itfornonprofits.models import Project
from itfornonprofits.models import Sector
from itfornonprofits.models import Skill
from itfornonprofits.models import Engineer

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
    p = Project(
        name=request.POST['name'],
        description=request.POST['description'],
        time_needed=request.POST['time_needed'],
        email=request.POST['email'],
        date_created=datetime.datetime.now()
    )
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

def viewproject(request):
    pk = idx(request.POST, 'pk')
    if pk == None:
        pk = idx(request.GET, 'pk')
    p = Project.objects.get(pk=int(pk))
    context = {'project': p}
    return render(request, 'itfornonprofits/viewproject.html', context);

def contactproject(request):
    p = Project.objects.get(pk=request.POST['pk'])
    message = """
From: {fromm}
To: {to}
Reply-to: {replyto}
Subject: {subject}

{message}
    """.format(
        fromm='noreply@itfornonprofits.sh',
        to=p.email,
        replyto=request.POST['email'],
        subject=request.POST['subject'],
        message=request.POST['message'],
    )
    try:
        mtpObj = smtplib.SMTP('localhost')
        smtpObj.sendmail(requuest.POST['email'], p.email, message)         
        message_to_user = "Successfully sent email"
    except smtplib.SMTPException:
        message_to_user = "Error: unable to send email"
    except:
        message_to_user = 'Error: Message not sent, because are not able to connect to mail server'
    context = {'project': p, 'message': message_to_user}
    return render(request, 'itfornonprofits/viewproject.html', context);

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

def viewengineers(request):
    objects = Engineer.objects
    mintime = int(idx(request.POST, 'mintime', '0'))
    sectors = [x.strip() for x in str(idx(request.POST, 'sectors', '')).split(',')]
    skills = [x.strip() for x in str(idx(request.POST, 'skills', '')).split(',')]
    if sectors == ['']:
        sectors = []
    if skills == ['']:
        skills = []
    if mintime > 0:
        objects = objects.filter(time_per_week__gte=mintime)
    if type(objects != list):
        objects = objects.all()
    if len(skills) > 0:
        objects = filter(lambda x: filter_list([y.name for y in x.skills.all()], skills), objects)
    if len(sectors) > 0:
        objects = filter(lambda x: filter_list([y.name for y in x.sectors.all()], sectors), objects)
    engineers = objects
    new_engineers = []
    for engineer in engineers:
        engineer.new_skills =  ', '.join([str(s.name) for s in engineer.skills.all()])
        engineer.new_sectors = ', '.join([str(s.name) for s in engineer.sectors.all()])
        engineer.time_available = engineer.time_per_week - engineer.time_per_week_alloted
        new_engineers.append(engineer)
    sectors_list = json.dumps(sorted([sector.name for sector in Sector.objects.all()]))
    skills_list = json.dumps(sorted([skill.name for skill in Skill.objects.all()]))
    context = {'engineers': new_engineers, 'sectors_list': sectors_list, 'skills_list': skills_list}
    print new_engineers
    return render(request, 'itfornonprofits/viewengineers.html', context)

def registerengineer(request):
    context = {}
    return render(request, 'itfornonprofits/registerengineer.html', context)

def createengineer(request):
    e = Engineer(
        name=request.POST['name'],
        description=request.POST['description'],
        time_per_week=request.POST['time_weekly'],
        time_per_week_alloted=0,
        email=request.POST['email'],
    )
    e.save()
    sectors = [x.strip() for x in str(idx(request.POST, 'sectors', '')).split(',')]
    for sector in sectors:
        project_sector = Sector.objects.filter(name=sector)
        if (len(project_sector) == 0):
            project_sector = Sector()
            project_sector.name = sector
            project_sector.save()
        else:
            project_sector = project_sector[0]
        e.sectors.add(project_sector)
    skills = [x.strip() for x in str(idx(request.POST, 'skills', '')).split(',')]
    for skill in skills:
        project_skill = Skill.objects.filter(name=skill)
        if (len(project_skill) == 0):
            project_skill = Skill()
            project_skill.name = skill
            project_skill.save()
        else:
            project_skill = project_skill[0]
        e.skills.add(project_skill)

    return render(request, 'itfornonprofits/viewengineers.html')

    context = {}
    return render(request, 'itfornonprofits/registerengineer.html', context)

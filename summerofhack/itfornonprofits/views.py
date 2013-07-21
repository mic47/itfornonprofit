from django.shortcuts import render
from django.http import HttpResponse
import json
import datetime
import email
import smtplib
import time
from itfornonprofits.models import Project
from itfornonprofits.models import Sector
from itfornonprofits.models import Skill
from itfornonprofits.models import Engineer

def index(request):
  #  num_projects = len(Project.objects.all())
    num_hours = sum([e.time_per_week - e.time_per_week_alloted for e in Engineer.objects.all()])
    num_projects = 2000000 - 1375383177 + int(time.time())
    context = {'num_projects': num_projects, 'num_hours': num_hours}
    return render(request, 'itfornonprofits/index.html', context)

def idx(d, v, default=None):
    if v in d:
        return d[v]
    return default

def idx_not_empty_string(d, v, default=None):
    ret = idx(d, v, default)
    if ret == '':
        return default
    return ret

def addproject(request):
    return render(request, 'itfornonprofits/addproject.html')

def createprojectindb(request):
    p = Project(
        name=request.POST['name'],
        description=request.POST['description'],
        time_needed=request.POST['time_needed'],
        email=request.POST['email'],
        fbpage=request.POST['fbpage'],
        status='New',
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
        project_skill = Skill.objects.filter(name=skill)
        if (len(project_skill) == 0):
            project_skill = Skill()
            project_skill.name = skill
            project_skill.save()
        else:
            project_skill = project_skill[0]
        p.skills.add(project_skill)

    return viewprojects(request)

def viewproject(request, pk):
    p = Project.objects.get(pk=int(pk))
    skills_list = json.dumps(sorted([skill.name for skill in Skill.objects.all()]))
    if p.status == 'Backed':
        backing_message = 'Project is backed by '
    elif p.status == 'Finished':
        backing_message = 'Project was finished by '
    else: 
        backing_message = 'Project is not backed yet.'
    context = {'project': p, 'skills_list': skills_list, 'engineers': Engineer.objects.all(), 'backing_message': backing_message}
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
        smtpObj.sendmail(request.POST['email'], p.email, message)         
        message_to_user = "Successfully sent email"
    except smtplib.SMTPException:
        message_to_user = "Error: unable to send email"
    except:
        message_to_user = 'Error: Message not sent, because are not able to connect to mail server'
    if project.status == 'Backed':
        backing_message = 'Project is backed by '
    elif project.status == 'Finished':
        backing_message = 'Project was finished by '
    else: 
<<<<<<< HEAD
        backing_message = 'Project is not backed yet.'
    context = {'project': p, 'message': message_to_user, 'backing_message': backing_message}
=======
        backing_message = 'Project is no backed yet.'
    context = {'project': p, 'message': message_to_user, 'backing_message': backing_message, 'engineers': Engineer.objects.all()}
>>>>>>> ef706c80690fea4bfaa5247fdf517ee172046121
    return render(request, 'itfornonprofits/viewproject.html', context);

def filter_list(wat, stuff):
    intersection = set(wat).intersection(set(stuff)) 
    return len(intersection) > 0 or len(wat) == 0

def order_status(x):
    if x.status == 'Finished':
        return 2
    if x.status == 'Backed':
        return 1
    return 0

def viewprojects(request):
    # Keyword search
    # Match na aspon jeden skill, aspon jeden vector
    objects = Project.objects
    maxtime = int(idx_not_empty_string(request.POST, 'maxtime', '100'))
    mintime = int(idx_not_empty_string(request.POST, 'mintime', '0'))
    keyword = str(idx(request.POST, 'keyword', ''))
    sectors = [x.strip() for x in str(idx(request.POST, 'sectors', '')).split(',')]
    skills = [x.strip() for x in str(idx(request.POST, 'skills', '')).split(',')]
    if sectors == ['']:
        sectors = []
    if skills == ['']:
        skills = []
    if maxtime > 0:
        objects = objects.filter(time_needed__lte=maxtime)
    if mintime > 0:
        objects = objects.filter(time_needed__gte=mintime)
    if len(keyword) > 0:
        objects = objects.filter(description__contains=keyword).order_by('-status')
    if type(objects != list):
        objects = objects.order_by('-status')
    if len(skills) > 0:
        objects = filter(lambda x: filter_list([y.name for y in x.skills.all()], skills), objects)
    if len(sectors) > 0:
        objects = filter(lambda x: filter_list([y.name for y in x.sectors.all()], sectors), objects)
    projects = objects
    new_projects = []
    for project in projects:
        project.new_skills =  ', '.join([str(s.name) for s in project.skills.all()])
        project.new_sectors = ', '.join([str(s.name) for s in project.sectors.all()])
        if len(project.description) > 100:
            project.description = project.description[:90] + '...'
        new_projects.append(project)
    sectors_list = json.dumps(sorted([sector.name for sector in Sector.objects.all()]))
    sectors = Sector.objects.all()
    skills_list = json.dumps(sorted([skill.name for skill in Skill.objects.all()]))
    skills = Skill.objects.all()
    new_projects = sorted(new_projects, key=order_status)
    context = {'projects': new_projects, 'sectors_list': sectors_list, 'skills_list': skills_list, 'sectors': sectors, 'skills': skills}
    return render(request, 'itfornonprofits/viewprojects.html', context)

def viewengineers(request):
    donated_hours = 0
    available_hours = 0
    for engineer in Engineer.objects.all():
        donated_hours += engineer.time_per_week_alloted
        available_hours += engineer.time_per_week - engineer.time_per_week_alloted
    objects = Engineer.objects
    mintime = int(idx_not_empty_string(request.POST, 'mintime', '0'))
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
        engineer.finished_projects = len(engineer.project_set.filter(status='Finished'))
    sectors_list = json.dumps(sorted([sector.name for sector in Sector.objects.all()]))
    skills_list = json.dumps(sorted([skill.name for skill in Skill.objects.all()]))
    sectors = Sector.objects.all()
    skills = Skill.objects.all()
    context = {'engineers': new_engineers, 'sectors_list': sectors_list, 'skills_list': skills_list, 'available_hours': available_hours, 'donated_hours': donated_hours, 'sectors': sectors, 'skills': skills}
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

    return viewengineers(request)

    context = {}
    return render(request, 'itfornonprofits/registerengineer.html', context)

def addskilltoproject(request, pk):
    skill = idx(request.POST, 'skills', '')
    project = Project.objects.get(pk=pk)
    try: 
        skill_obj = Skill.objects.get(name=skill)
    except:
        #TODO: correct exception hadnling
        skill_obj = Skill(name=skill)
        skill_obj.save()
    project.skills.add(skill_obj)
    project.save()
   
    skills_list = json.dumps(sorted([skill.name for skill in Skill.objects.all()]))
    if project.status == 'Backed':
        backing_message = 'Project is backed by '
    elif project.status == 'Finished':
        backing_message = 'Project was finished by '
    else: 
        backing_message = 'Project is no backed yet.'
    print backing_message, project.status, 'asdf'
    context = {'project': project, 'skills_list': skills_list, 'backing_message': backing_message, 'engineers': Engineer.objects.all()}
    return render(request, 'itfornonprofits/viewproject.html', context);
   
def backproject(request, pk_project, pk_user):
    project = Project.objects.get(pk=int(pk_project))
    user = Engineer.objects.get(pk=int(pk_user))
    if project.status != 'Finished':
        project.status = 'Backed'
        project.backed_by.add(user)
        project.save()
    return HttpResponse("Hello world")

def finishproject(request, pk_project):
    project = Project.objects.get(pk=int(pk_project))
    project.status = 'Finished'
    project.save()
    return HttpResponse("Hello world")

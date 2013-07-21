from django.db import models

class Skill(models.Model):
    def __unicode__(self):
        return self.name

    name = models.CharField(max_length=200)

class Sector(models.Model):
    def __unicode__(self):
        return self.name
        
    name = models.CharField(max_length=200)

class Project(models.Model):
    def __unicode__(self):
        return self.name

    name = models.CharField(max_length=200)
    description = models.TextField()
    date_created = models.DateTimeField('date added')
    time_needed = models.IntegerField()
    skills = models.ManyToManyField(Skill)
    sectors = models.ManyToManyField(Sector)
    email = models.EmailField(max_length=300)

class Engineer(models.Model):
    def __unicode__(self):
        return self.name

    name = models.CharField(max_length=200)
    description = models.TextField()
    sectors = models.ManyToManyField(Sector)
    skills = models.ManyToManyField(Skill)
    email = models.EmailField(max_length=300)
    time_per_week = models.IntegerField()
    time_per_week_alloted = models.IntegerField()

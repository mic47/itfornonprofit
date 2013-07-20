from django.db import models

class Project(models.Model):
	def __unicdode__(self):
		return self.name

	name = models.CharField(max_length=200)
	description = models.TextField()
	date_created = models.DateTimeField('date added')
	time_needed = models.IntegerField()

class Skill(models.Model):
	def __unicdode__(self):
		return self.name

	name = models.CharField(max_length=200)
	projects = models.ManyToManyField(Project)

class Sector(models.Model):
	def __unicdode__(self):
		return self.name
		
	name = models.CharField(max_length=200)
	projects = models.ManyToManyField(Project)

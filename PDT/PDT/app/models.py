"""
Definition of models.
"""

from django.db import models
from django import forms

# Create your models here.

class ProjectManager(models.Model):
    mid = models.AutoField("Manager ID", primary_key=True)
    name = models.CharField("Manager Name", max_length=50)

class Developer(models.Model):
    workerid = models.AutoField("Developer ID", primary_key=True)
    name = models.CharField("Developer Name", max_length=50)

class Project(models.Model):
    pid = models.AutoField("Project ID", primary_key=True)
    name = models.CharField("Project Name", max_length=200)
    developerid = models.PositiveIntegerField(null=True)

class Iteration(models.Model):
    iterid = models.AutoField(primary_key=True)
    iternumber = models.PositiveIntegerField("Iteration no")
    timecost = models.PositiveIntegerField(default=0)
    phrase = models.CharField("Phrase", max_length=50)
    projectid = models.PositiveIntegerField(null=True)
    laststart = models.TimeField(blank=True, null=True)
    lastend = models.TimeField(blank=True, null=True)
    
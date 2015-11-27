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

    def __str__(self):
        return self.name

class Project(models.Model):
    pid = models.AutoField("Project ID", primary_key=True)
    name = models.CharField("Project Name", max_length=200)
    developers = models.ManyToManyField(Developer)
    phase = models.IntegerField(default=0)
    iterations = models.IntegerField(default=0)
    expectedsloc = models.IntegerField(default=0)
    totaltime = models.PositiveIntegerField(null=True)
    totalsloc = models.PositiveIntegerField(null=True)

class Iteration(models.Model):
    iterid = models.AutoField(primary_key=True)
    iternumber = models.PositiveIntegerField("Iteration no.")
    timecost = models.PositiveIntegerField(default=0)
    phrase = models.CharField("Phase", max_length=50)
    projectid = models.PositiveIntegerField("Project ID", null=True)
    laststart = models.TimeField(blank=True, null=True)
    lastend = models.TimeField(blank=True, null=True)
    sloc = models.IntegerField(default=0)

class Defect(models.Model):
    defid = models.AutoField(primary_key=True)
    founditer = models.PositiveIntegerField('Iteration Found', null=True)
    removediter = models.PositiveIntegerField('Iteration Removed', null=True)
    description = models.CharField('Defect Description', max_length=200)
    timecost = models.PositiveIntegerField(default=0)
    laststart = models.TimeField(blank=True, null=True)
    lastend = models.TimeField(blank=True, null=True)

#Model Forms
class ProjectForm(forms.ModelForm):
    class Meta:
        model=Project
        fields = ['name' ,'developers','phase', 'iterations', 'expectedsloc']

class IterationForm(forms.ModelForm):
    class Meta:
        model = Iteration
        fields = ['phrase','iternumber','projectid']

class SLOCForm(forms.Form):
    sloc = forms.IntegerField();

class DefectForm(forms.Form):
    founditer = forms.IntegerField();
    removediter = forms.IntegerField();
    description = forms.CharField();

class EditProjectForm(forms.Form):
    name = forms.CharField();
    phase = forms.IntegerField();
    iterations = forms.IntegerField();
    expectedsloc = forms.IntegerField();

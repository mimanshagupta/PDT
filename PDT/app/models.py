"""
Definition of models.
"""

from django.db import models
from django import forms
from django.db.models import Max
from django.db.models import Sum

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
    phase = models.PositiveIntegerField(default=0)
    iterations = models.IntegerField(default=0)
    expectedsloc = models.IntegerField(default=0)
    expectedduration = models.IntegerField(default=0)
    totaltime = models.PositiveIntegerField(default=0)
    totalsloc = models.PositiveIntegerField(default=0)

    def getprojectpercentsloc(self):
        iteration = Iteration.objects.filter(projectid=self.pid).latest('iterid')
        return (iteration.sloc / self.expectedsloc) * 100

    def getprojecteffort(self):
        iterations = Iteration.objects.filter(projectid=self.pid)
        project_effort = 0
        for iteration in iterations:
            project_effort = project_effort + ((iteration.timecost/2592000) * self.developers.count())
        return (project_effort / self.expectedduration) * 100

    def getprojectdeliveredsloc(self):
        iterationmax = Iteration.objects.filter(projectid=self.pid).latest('iterid')
        iterations = Iteration.objects.filter(projectid=self.pid)
        project_effort = 0
        for iteration in iterations:
            project_effort = project_effort + ((iteration.timecost/2592000) * self.developers.count())

        project_deliveredsloc = iterationmax.sloc / project_effort
        return project_deliveredsloc

    def getprojectdefectsinjected(self):
        defect = Defect.objects.filter(projectid = self.pid)
        return defect.count()

    def getprojectdefectsremoved(self):
        defect = Defect.objects.filter(projectid = self.pid)
        return defect.count()

    def getinjectionrate(self):
        defect = Defect.objects.filter(projectid = self.pid)
        defect_count = defect.count()
        iterations = Iteration.objects.filter(projectid=self.pid)
        timecost = 0

        for iteration in iterations:
            timecost += (iteration.timecost/3600)

        return defect_count / (timecost * self.developers.count() )

    def getremovalrate(self):
        defect = Defect.objects.filter(projectid = self.pid)
        defect_count = defect.count()
        iterations = Iteration.objects.filter(projectid=self.pid)
        timecost = 0

        for iteration in iterations:
            timecost += (iteration.defect_timecost/3600)

        return defect_count / (timecost * self.developers.count() )


class Phase(models.Model):
    phaseid = models.AutoField(primary_key=True)
    projectid = models.PositiveIntegerField("Project ID", null=True)
    PHASE_CHOICES = (
    ('inception', 'inception'),
    ('elaboration', 'elaboration'),
    ('construction', 'construction'),
    ('transition', 'transition'),
    )
    phase_name = models.CharField("Phase Name", choices=PHASE_CHOICES, max_length=200)

    def getphasepercentsloc(self):
        project = Project.objects.get(pk=self.projectid)
        iteration = Iteration.objects.filter(projectid=self.projectid, phrase=self.phase_name).latest('iterid')
        return (iteration.sloc / project.expectedsloc) * 100

    def getphaseeffort(self):
        project = Project.objects.get(pk=self.projectid)
        iterations = Iteration.objects.filter(projectid=self.projectid,phrase=self.phase_name)
        phase_effort = 0
        for iteration in iterations:
            phase_effort = phase_effort + ((iteration.timecost/2592000) * project.developers.count())

        return (phase_effort / project.expectedduration) * 100

    def getphasedeliveredsloc(self):
        project = Project.objects.get(pk=self.projectid)
        iterations = Iteration.objects.filter(projectid=self.projectid,phrase=self.phase_name)
        phase_delivered_sloc = 0
        for iteration in iterations:
            if iteration.timecost == 0:
                phase_delivered_sloc += 0
            else:
                phase_delivered_sloc = phase_delivered_sloc + (iteration.sloc / ((iteration.timecost/2592000) * project.developers.count()))

        return phase_delivered_sloc

    def getphasedefectsinjected(self):
        defect = Defect.objects.filter(projectid = self.projectid, injectedphase = self.phase_name)
        return defect.count()

    def getphasedefectsremoved(self):
        defect = Defect.objects.filter(projectid = self.projectid, removedphase = self.phase_name)
        return defect.count()

    def getinjectionrate(self):
        defect = Defect.objects.filter(projectid = self.projectid, injectedphase = self.phase_name)
        project = Project.objects.get(pk=self.projectid)
        defect_count = defect.count()
        iterations = Iteration.objects.filter(projectid=self.projectid, phrase=self.phase_name)
        timecost = 0

        for iteration in iterations:
            timecost += (iteration.timecost/3600)
        if timecost == 0:
            return 0
        else:
            return defect_count / (timecost * project.developers.count() )

    def getremovalrate(self):
        defect = Defect.objects.filter(projectid = self.projectid, removedphase = self.phase_name)
        project = Project.objects.get(pk=self.projectid)
        defect_count = defect.count()
        iterations = Iteration.objects.filter(projectid=self.projectid, phrase=self.phase_name)
        timecost = 0

        for iteration in iterations:
            timecost += (iteration.defect_timecost/3600)
        if timecost == 0:
            return 0
        else:
            return defect_count / (timecost * project.developers.count() )


class Iteration(models.Model):
    iterid = models.AutoField(primary_key=True)
    iternumber = models.PositiveIntegerField("Iteration no.")
    timecost = models.PositiveIntegerField(default=0)
    phrase = models.CharField("Phase (Please enter as \"inception\", \"elaboration\", \"construction\", \"transition\")", max_length=50)
    projectid = models.PositiveIntegerField("Project ID", null=True)
    laststart = models.TimeField(blank=True, null=True)
    lastend = models.TimeField(blank=True, null=True)
    defect_laststart = models.TimeField(blank=True, null=True)
    defect_lastend = models.TimeField(blank=True, null=True)
    sloc = models.IntegerField(default=0)
    defect_timecost = models.PositiveIntegerField(default=0)
    status = models.BooleanField(default = True)

    def getdefectsinjected(self):
        defect = Defect.objects.filter(projectid = self.projectid, injectedphase = self.phrase, injectediter = self.iternumber)
        return defect.count()

    def getdefectsremoved(self):
        defect = Defect.objects.filter(projectid = self.projectid, removedphase = self.phrase, removediter = self.iternumber)
        return defect.count()

    def getpercentsloc(self):
        project = Project.objects.get(pk=self.projectid)
        return (self.sloc / project.expectedsloc) * 100

    def geteffort(self):
        project = Project.objects.get(pk=self.projectid)
        return (((self.timecost/2592000) * project.developers.count())/project.expectedduration) * 100

    def getdeliveredsloc(self):
        project = Project.objects.get(pk=self.projectid)
        if self.timecost == 0:
            return 0
        else:
            return self.sloc / ((self.timecost/2592000) * project.developers.count())

    def getinjectionrate(self):
        defect = Defect.objects.filter(projectid = self.projectid, injectedphase = self.phrase, injectediter = self.iternumber)
        project = Project.objects.get(pk=self.projectid)
        defect_count = defect.count()
        if self.timecost == 0:
            return 0
        else:
            return defect_count / ((self.timecost / 3600) * project.developers.count() )

    def getremovalrate(self):
        defect = Defect.objects.filter(projectid = self.projectid, removedphase = self.phrase, removediter = self.iternumber)
        project = Project.objects.get(pk=self.projectid)
        defect_count = defect.count()
        if self.defect_timecost == 0:
            return 0
        else:
            return defect_count / ((self.defect_timecost / 3600) * project.developers.count() )

class Defect(models.Model):
    defid = models.AutoField(primary_key=True)
    projectid = models.PositiveIntegerField('Project ID', null=True)
    injectediter = models.PositiveIntegerField('Iteration Injected', null=True)
    removediter = models.PositiveIntegerField('Iteration Removed', null=True)
    description = models.CharField('Defect Description', max_length=200, null=True)
    DEFECT_CHOICES = (
    ('requirement', 'requirement'),
    ('design', 'design'),
    ('implementation', 'implementation'),
    ('badfix', 'badfix'),
    )

    PHASE_CHOICES = (
    ('inception', 'inception'),
    ('elaboration', 'elaboration'),
    ('construction', 'construction'),
    ('transition', 'transition'),
    )

    injectedphase = models.CharField('Phase Injected', choices=PHASE_CHOICES, max_length=200, null=True)
    removedphase = models.CharField('Phase Removed', choices=PHASE_CHOICES, max_length=200, null=True)
    resolved_by = models.OneToOneField(Developer, null=True)
    defect_type = models.CharField('Defect Type', choices=DEFECT_CHOICES, max_length=200, null=True)

#Model Forms
class ProjectForm(forms.ModelForm):
    class Meta:
        model=Project
        fields = ['name' ,'developers','phase', 'iterations', 'expectedsloc', 'expectedduration']

class IterationForm(forms.ModelForm):
    class Meta:
        model = Iteration
        fields = ['phrase','iternumber','projectid']

class SLOCForm(forms.Form):
    sloc = forms.IntegerField();

class DefectForm(forms.ModelForm):
    class Meta:
        model=Defect
        fields = ['injectedphase', 'injectediter', 'removedphase', 'removediter','description', 'resolved_by', 'defect_type']

class EditProjectForm(forms.Form):
    name = forms.CharField();
    phase = forms.IntegerField();
    iterations = forms.IntegerField();
    expectedsloc = forms.IntegerField();

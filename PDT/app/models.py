"""
Definition of models.
"""

from django.db import models
from django import forms
from django.db.models import Max
from django.db.models import Sum
from django.core.validators import MaxValueValidator, MinValueValidator

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
    phase = models.PositiveIntegerField(default=1,
        validators=[
            MaxValueValidator(4),
            MinValueValidator(1)
        ])
    iterations = models.IntegerField(default=0)
    expectedsloc = models.IntegerField(default=0)
    expectedduration = models.IntegerField(default=0)
    defaultyield = models.IntegerField(default = 80)
    totaltime = models.PositiveIntegerField(default=0)
    totalsloc = models.PositiveIntegerField(default=0)

    def getprojectpercentsloc(self):
        iteration = Iteration.objects.filter(projectid=self.pid).latest('iterid')
        return format((iteration.sloc / self.expectedsloc) * 100, '.2f')

    def getprojecteffort(self):
        iterations = Iteration.objects.filter(projectid=self.pid)
        project_effort = 0
        for iteration in iterations:
            project_effort = project_effort + ((iteration.timecost/2592000) * self.developers.count())
        return format((project_effort / self.expectedduration) * 100, '.2f')

    def getprojectdeliveredsloc(self):
        iterationmax = Iteration.objects.filter(projectid=self.pid).latest('iterid')
        iterations = Iteration.objects.filter(projectid=self.pid)
        project_effort = 0
        for iteration in iterations:
            project_effort = project_effort + ((iteration.timecost/2592000) * self.developers.count())

        if project_effort == 0:
            return 0
        else:
            project_deliveredsloc = iterationmax.sloc / project_effort
            return format(project_deliveredsloc, '.2f')

    def getprojectdefectsinjected(self):
        defects = Defect.objects.filter(projectid = self.pid)
        for defect in defects:
            print(defect.description)
        return defects.count()

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

        if timecost == 0:
            return 0
        else:
            return format(defect_count / (timecost * self.developers.count() ), '.2f')

    def getremovalrate(self):
        defect = Defect.objects.filter(projectid = self.pid)
        defect_count = defect.count()
        iterations = Iteration.objects.filter(projectid=self.pid)
        timecost = 0

        for iteration in iterations:
            timecost += (iteration.defect_timecost/3600)

        if timecost == 0:
            return 0
        else:
            return format(defect_count / (timecost * self.developers.count() ), '.2f')

    def getdefectsperksloc(self):
        defect = Defect.objects.filter(projectid = self.pid)
        iteration = Iteration.objects.filter(projectid=self.pid).latest('iterid')
        remaining_defects = (100 - self.defaultyield) * defect.count()
        if iteration.sloc == 0:
            return 0
        else:
            defectsperksloc = remaining_defects / (iteration.sloc/1000)
            return format(defectsperksloc, '.2f')

    def getyield(self):
        removeddefects = Defect.objects.filter(projectid = self.pid)
        injecteddefects = Defect.objects.filter(projectid = self.pid)
        project = Project.objects.get(pk = self.pid)
        phaseyield = 0
        if injecteddefects.count() == 0:
            return 0
        else:
            phaseyield = (removeddefects.count() / injecteddefects.count()) * 100
            return phaseyield


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
        return format((iteration.sloc / project.expectedsloc) * 100, '.2f')

    def getphaseeffort(self):
        project = Project.objects.get(pk=self.projectid)
        iterations = Iteration.objects.filter(projectid=self.projectid,phrase=self.phase_name)
        phase_effort = 0
        for iteration in iterations:
            phase_effort = phase_effort + ((iteration.timecost/2592000) * project.developers.count())

        return format((phase_effort / project.expectedduration) * 100, '.2f')

    def getphasedeliveredsloc(self):
        project = Project.objects.get(pk=self.projectid)
        iterations = Iteration.objects.filter(projectid=self.projectid,phrase=self.phase_name)
        phase_delivered_sloc = 0
        for iteration in iterations:
            if iteration.timecost == 0:
                phase_delivered_sloc += 0
            else:
                phase_delivered_sloc = phase_delivered_sloc + (iteration.sloc / ((iteration.timecost/2592000) * project.developers.count()))

        return format(phase_delivered_sloc, '.2f')

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
            return format(defect_count / (timecost * project.developers.count() ), '.2f')

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
            return format(defect_count / (timecost * project.developers.count() ), '.2f')

    def getdefectsperksloc(self):
        defect = Defect.objects.filter(projectid = self.projectid, injectedphase = self.phase_name)
        project = Project.objects.get(pk=self.projectid)
        iteration = Iteration.objects.filter(projectid=self.projectid, phrase=self.phase_name).latest('iterid')
        remaining_defects = (100 - project.defaultyield) * defect.count()
        if iteration.sloc == 0:
            return 0
        else:
            defectsperksloc = remaining_defects / (iteration.sloc/1000)
            return format(defectsperksloc, '.2f')

    def getyield(self):
        removeddefects = Defect.objects.filter(projectid = self.projectid, removedphase = self.phase_name)
        injecteddefects = Defect.objects.filter(projectid = self.projectid, injectedphase = self.phase_name)
        project = Project.objects.get(pk=self.projectid)
        phaseyield = 0
        if injecteddefects.count() == 0:
            return 0
        else:
            phaseyield = (removeddefects.count() / injecteddefects.count()) * 100
            return phaseyield


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
        return format((self.sloc / project.expectedsloc) * 100, '.2f')

    def geteffort(self):
        project = Project.objects.get(pk=self.projectid)
        effort = ((self.timecost/2592000) * project.developers.count()) / project.expectedduration
        return format(effort * 100, '.2f')

    def getdeliveredsloc(self):
        project = Project.objects.get(pk=self.projectid)
        if self.timecost == 0:
            return 0
        else:
            return format(( self.sloc / ((self.timecost/2592000) * project.developers.count())), '.2f')

    def getinjectionrate(self):
        defect = Defect.objects.filter(projectid = self.projectid, injectedphase = self.phrase, injectediter = self.iternumber)
        project = Project.objects.get(pk=self.projectid)
        defect_count = defect.count()
        if self.timecost == 0:
            return 0
        else:
            return format(defect_count / ((self.timecost / 3600) * project.developers.count() ), '.2f')

    def getremovalrate(self):
        defect = Defect.objects.filter(projectid = self.projectid, removedphase = self.phrase, removediter = self.iternumber)
        project = Project.objects.get(pk=self.projectid)
        defect_count = defect.count()
        if self.defect_timecost == 0:
            return 0
        else:
            return format(defect_count / ((self.defect_timecost / 3600) * project.developers.count() ), '.2f')

    def getdefectsperksloc(self):
        defect = Defect.objects.filter(projectid = self.projectid, injectedphase = self.phrase, injectediter = self.iternumber)
        project = Project.objects.get(pk=self.projectid)
        remaining_defects = (100 - project.defaultyield) * defect.count()
        if self.sloc == 0:
            return 0
        else:
            defectsperksloc = remaining_defects / (self.sloc/1000)
            return format(defectsperksloc, '.2f')

    def getyield(self):
        removeddefects = Defect.objects.filter(projectid = self.projectid, removedphase = self.phrase, removediter = self.iternumber)
        injecteddefects = Defect.objects.filter(projectid = self.projectid, injectedphase = self.phrase, injectediter = self.iternumber)
        project = Project.objects.get(pk=self.projectid)
        iterationyield = 0
        if injecteddefects.count() == 0:
            return 0
        else:
            iterationyield = (removeddefects.count() / injecteddefects.count()) * 100
            return iterationyield


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
        fields = ['name' ,'developers','phase', 'iterations', 'expectedsloc', 'expectedduration', 'defaultyield']

class IterationForm(forms.ModelForm):
    class Meta:
        model = Iteration
        fields = ['phrase','iternumber','projectid']

class SLOCForm(forms.Form):
    sloc = forms.IntegerField();

class DefectForm(forms.ModelForm):
    class Meta:
        model=Defect
        fields = ['projectid', 'injectedphase', 'injectediter', 'removedphase', 'removediter','description', 'resolved_by', 'defect_type']

class EditProjectForm(forms.Form):
    name = forms.CharField();
    phase = forms.IntegerField();
    iterations = forms.IntegerField();
    expectedsloc = forms.IntegerField();

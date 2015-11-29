"""
Definition of views.
"""

from django.shortcuts import render, render_to_response
from django.http import HttpRequest, HttpResponse, HttpResponseRedirect
from django.template import RequestContext
from datetime import datetime, timedelta
from django.db.models import *
from app.models import *

def home(request):
    """Renders the home page."""
    assert isinstance(request, HttpRequest)
    return render(
        request,
        'app/index.html',
        context_instance = RequestContext(request,
        {
            'title':'Welcome',
            'year':datetime.now().year
        })
    )

def managerhome(request):
    projectlist = Project.objects.all()
    return render_to_response('app/managerhome.html', {'projectlist': projectlist},
                              context_instance = RequestContext(request,
        {
            'title':'Home',
            'year':datetime.now().year
        }))

def createproject(request):
    if request.method == 'GET':
        form = ProjectForm()
        return render(request, 'app/create.html', {'form': form})
    elif request.method == 'POST':
        form = ProjectForm(request.POST)
        if form.is_valid():
            numberofphases = form.cleaned_data['phase']
            if numberofphases > 0:
                phase = Phase(projectid = Project.objects.count() + 1 , phase_name = 'inception')
                phase.save()
            if numberofphases > 1:
                phase = Phase(projectid = Project.objects.count() + 1 , phase_name = 'elaboration')
                phase.save()
            if numberofphases > 2:
                phase = Phase(projectid = Project.objects.count() + 1 , phase_name = 'construction')
                phase.save()
            if numberofphases > 3:
                phase = Phase(projectid = Project.objects.count() + 1 , phase_name = 'transition')
                phase.save()

        form.save()
        return HttpResponseRedirect('/manager')

def createiteration(request,pid):
    if request.method == 'GET':
        form = IterationForm()
        return render(request, 'app/create.html', {'form': form})
    elif request.method == 'POST':
        form = IterationForm(request.POST)
        if form.is_valid():
            iteration = Iteration(iternumber=form.cleaned_data['iternumber'], phrase = form.cleaned_data['phrase'], projectid = form.cleaned_data['projectid'])
            iteration.save()
            return HttpResponseRedirect('/project/analysis/%s' %pid)

        return HttpResponseRedirect('/project/analysis/%s' %pid)

def itrdetail(request, iterid):
    itr = Iteration.objects.get(pk=iterid)
    if request.method == 'GET':
        form = SLOCForm()
        return render_to_response('app/iterationdetail.html',{'itr': itr, 'form': form},
                              context_instance = RequestContext(request,
        {
            'title':'Iteration Detail',
            'year':datetime.now().year
        }))
    elif request.method == 'POST':
        form = SLOCForm(request.POST)
        if form.is_valid():
            itr.sloc = form.cleaned_data['sloc']
            itr.save()
        return HttpResponseRedirect('/project/analysis/%s' %itr.projectid)


def projectanalysis(request, pid):
    project = Project.objects.get(pk=pid)
    developers = project.developers.all()
    developerno = project.developers.count()
    slocsum = Iteration.objects.filter(projectid = pid).aggregate(Sum("sloc"))
    expectedsloc = project.expectedsloc
    phase = project.phase

    inception = Iteration.objects.filter(projectid=pid,phrase='inception')
    elaboration = Iteration.objects.filter(projectid=pid,phrase='elaboration')
    construction = Iteration.objects.filter(projectid=pid,phrase='construction')
    translation = Iteration.objects.filter(projectid=pid,phrase='translation')

    return render_to_response('app/projectanalysis.html',{'project':project, 'slocsum':slocsum, 'developerno':developerno, 'developers':developers, 'expectedsloc':expectedsloc, 'phase':phase ,'inception':inception, 'elaboration':elaboration, 'construction':construction, 'translation':translation},
                              context_instance = RequestContext(request,
        {
            'title':'Analysis',
            'year':datetime.now().year
        }))

def metrics(request, pid):
    project = Project.objects.get(pk=pid)

    developerno = project.developers.count()

    slocsum = Iteration.objects.filter(projectid = pid).aggregate(Sum("sloc"))
    expectedsloc = project.expectedsloc

    inception_phase = Phase.objects.get(projectid=pid,phase_name='inception')
    elaboration_phase = Phase.objects.get(projectid=pid,phase_name='elaboration')
    construction_phase = Phase.objects.get(projectid=pid,phase_name='construction')
    transition_phase = Phase.objects.get(projectid=pid,phase_name='transition')

    inception = Iteration.objects.filter(projectid=pid,phrase='inception')
    elaboration = Iteration.objects.filter(projectid=pid,phrase='elaboration')
    construction = Iteration.objects.filter(projectid=pid,phrase='construction')
    transition = Iteration.objects.filter(projectid=pid,phrase='transition')

    #inception_sum = Iteration.objects.filter(projectid=pid,phrase='inception').aggregrate(Sum("sloc"))

    return render_to_response('app/viewmetrics.html',{'project':project, 'slocsum':slocsum, 'developerno':developerno, 'expectedsloc':expectedsloc, 'inception':inception, 'elaboration':elaboration, 'construction':construction, 'transition':transition, 'inception_phase':inception_phase, 'elaboration_phase':elaboration_phase, 'construction_phase':construction_phase, 'transition_phase':transition_phase},
                              context_instance = RequestContext(request,
        {
            'title':'Viewmetrics',
            'year':datetime.now().year
        }))

def editproject(request, pid):
    project = Project.objects.get(pk=pid)
    developers = project.developers.all()
    if request.method == 'GET':
        return render_to_response('app/editproject.html',{'project':project, 'developers':developers},
                              context_instance = RequestContext(request,
        {
            'title':'Edit',
            'year':datetime.now().year
        }))
    elif request.method == 'POST':
        form = EditProjectForm(request.POST)
        if form.is_valid():
            project = Project.objects.get(pk=pid)
            project.name = form.cleaned_data['name']
            project.phase = form.cleaned_data['phase']
            project.iterations = form.cleaned_data['iterations']
            project.expectedsloc = form.cleaned_data['expectedsloc']
            project.save()
        return HttpResponseRedirect('/manager')

def developers(request):
    developers = Developer.objects.all()
    return render_to_response('app/developerlist.html',{'developers':developers},
                              context_instance = RequestContext(request,
        {
            'title':'Login',
            'year':datetime.now().year
        }))

def developerhome(request, workerid):
    projects = Project.objects.filter(developers__workerid=workerid)
    return render_to_response('app/developerhome.html',{'projects':projects},
                              context_instance = RequestContext(request,
        {
            'title':'Home',
            'year':datetime.now().year
        }))

def projectdetail(request, pid):
    project = Project.objects.get(pk=pid)
    inception = Iteration.objects.filter(projectid=pid,phrase='inception')
    elaboration = Iteration.objects.filter(projectid=pid,phrase='elaboration')
    construction = Iteration.objects.filter(projectid=pid,phrase='construction')
    translation = Iteration.objects.filter(projectid=pid,phrase='translation')
    if request.method == 'GET':
        form = DefectForm()
        return render_to_response('app/projectdetail.html',{'form':form, 'project':project, 'inception':inception, 'elaboration':elaboration, 'construction':construction, 'translation':translation},
                              context_instance = RequestContext(request,
        {
            'title':'Phrases and Iterations',
            'year':datetime.now().year
        }))
    elif request.method == 'POST':
        form = DefectForm(request.POST)
        if form.is_valid():
            defect = Defect(description = form.cleaned_data['description'], founditer = form.cleaned_data['founditer'], removediter = form.cleaned_data['removediter'])
            defect.save()
            print(defect)
        return HttpResponseRedirect('/project/%s' %pid)


def iterationpage(request, iterid):
    iteration = Iteration.objects.get(pk=iterid)
    project = Project.objects.get(pk=iteration.projectid)
    displayhour = int(iteration.timecost/3600)
    displaymin = int((iteration.timecost - displayhour*3600)/60)
    displaysec = int(iteration.timecost - displayhour*3600 - displaymin*60)
    return render_to_response('app/iteration.html', {'iteration':iteration, 'project':project,'displayhour':displayhour, 'displaymin':displaymin, 'displaysec':displaysec},
                              context_instance = RequestContext(request,
        {
            'title':'Iteration detail',
            'year':datetime.now().year
        }))

def startitimer(request, iterid):
    iteration = Iteration.objects.get(pk=iterid)
    project = Project.objects.get(pk=iteration.projectid)
    start = datetime.now()
    iteration.laststart = start
    iteration.save()
    return HttpResponseRedirect('/project/iteration/%s/timer' % iterid)

def itertimer(request, iterid):
    iteration = Iteration.objects.get(pk=iterid)
    project = Project.objects.get(pk=iteration.projectid)
    return render_to_response('app/itertimer.html', {'iteration':iteration, 'project':project},
                              context_instance = RequestContext(request,
        {
            'title':'Timer',
            'year':datetime.now().year
        }))

def enditimer(request, iterid):
    iteration = Iteration.objects.get(pk=iterid)
    project = Project.objects.get(pk=iteration.projectid)
    end = datetime.now()
    start = iteration.laststart
    hour = end.hour - start.hour
    minute = end.minute - start.minute
    sec = end.second - start.second
    iteration.lastend = end
    iteration.timecost += hour*3600 + minute*60 + sec
    project.totaltime += hour*3600 + minute*60 + sec
    iteration.save()
    project.save()
    return HttpResponseRedirect('/project/iteration/%s' % iterid)

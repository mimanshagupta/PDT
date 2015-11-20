"""
Definition of views.
"""

from django.shortcuts import render, render_to_response
from django.http import HttpRequest, HttpResponse, HttpResponseRedirect
from django.template import RequestContext
from datetime import datetime, timedelta
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

def projectanalysis(request, pid):
    project = Project.objects.get(pk=pid)
    inception = Iteration.objects.filter(projectid=pid,phrase='inception')
    elaboration = Iteration.objects.filter(projectid=pid,phrase='elaboration')
    construction = Iteration.objects.filter(projectid=pid,phrase='construction')
    translation = Iteration.objects.filter(projectid=pid,phrase='translation')
    return render_to_response('app/projectanalysis.html',{'project':project, 'inception':inception, 'elaboration':elaboration, 'construction':construction, 'translation':translation}, 
                              context_instance = RequestContext(request,
        {
            'title':'Analysis',
            'year':datetime.now().year
        }))


def developers(request):
    developers = Developer.objects.all()
    return render_to_response('app/developerlist.html',{'developers':developers}, 
                              context_instance = RequestContext(request,
        {
            'title':'Login',
            'year':datetime.now().year
        }))

def developerhome(request, workerid):
    projects = Project.objects.filter(developerid=workerid)
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
    return render_to_response('app/projectdetail.html',{'project':project, 'inception':inception, 'elaboration':elaboration, 'construction':construction, 'translation':translation}, 
                              context_instance = RequestContext(request,
        {
            'title':'Phrases and Iterations',
            'year':datetime.now().year
        }))

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
    min = end.minute - start.minute
    sec = end.second - start.second
    iteration.lastend = end
    iteration.timecost += hour*3600 + min*60 + sec
    iteration.save()
    return HttpResponseRedirect('/project/iteration/%s' % iterid)

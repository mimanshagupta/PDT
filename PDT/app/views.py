"""
Definition of views.
"""

from django.shortcuts import render, render_to_response
from django.http import HttpRequest, HttpResponse, HttpResponseRedirect
from django.template import RequestContext
from datetime import datetime, timedelta
from django.db.models import *
from app.models import *
from django.core.context_processors import csrf
from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from django.contrib import messages

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

def changetime(request, iterid):
    iteration = Iteration.objects.get(pk=iterid)
    if request.method == 'GET':
        form = ItertimeForm()
        return render_to_response('app/changetime.html',{'iteration': iteration, 'form': form},
                              context_instance = RequestContext(request,
        {
            'title':'Iteration Change Time',
            'year':datetime.now().year
        }))
    elif request.method == 'POST':
        form = ItertimeForm(request.POST)
        if form.is_valid():
            hours = form.cleaned_data['hours']
            minutes = form.cleaned_data['minutes']
            seconds = form.cleaned_data['seconds']
            iteration.timecost = hours*3600 + minutes*60 + seconds
            iteration.save()
        return HttpResponseRedirect('/manager/iteration/%s' %iterid)

def dchangetime(request, iterid):
    iteration = Iteration.objects.get(pk=iterid)
    if request.method == 'GET':
        form = DefecttimeForm()
        return render_to_response('app/changetime.html',{'iteration': iteration, 'form': form},
                              context_instance = RequestContext(request,
        {
            'title':'Iteration Change Defect Time',
            'year':datetime.now().year
        }))
    elif request.method == 'POST':
        form = DefecttimeForm(request.POST)
        if form.is_valid():
            hours = form.cleaned_data['hours']
            minutes = form.cleaned_data['minutes']
            seconds = form.cleaned_data['seconds']
            iteration.defect_timecost = hours*3600 + minutes*60 + seconds
            iteration.save()
        return HttpResponseRedirect('/manager/iteration/%s' %iterid)

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
    transition = Iteration.objects.filter(projectid=pid,phrase='transition')

    return render_to_response('app/projectanalysis.html',{'project':project, 'slocsum':slocsum, 'developerno':developerno, 'developers':developers, 'expectedsloc':expectedsloc, 'phase':phase ,'inception':inception, 'elaboration':elaboration, 'construction':construction, 'transition':transition},
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

    inception_phase = Phase.objects.filter(projectid=pid,phase_name='inception')
    elaboration_phase = Phase.objects.filter(projectid=pid,phase_name='elaboration')
    construction_phase = Phase.objects.filter(projectid=pid,phase_name='construction')
    transition_phase = Phase.objects.filter(projectid=pid,phase_name='transition')

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
    transition = Iteration.objects.filter(projectid=pid,phrase='transition')
    defects = Defect.objects.filter(projectid=pid)
    if request.method == 'GET':
        form = DefectForm()
        return render_to_response('app/projectdetail.html',{'form':form, 'project':project, 'inception':inception, 'elaboration':elaboration, 'construction':construction, 'transition':transition},
                              context_instance = RequestContext(request,
        {
            'title':'Phrases and Iterations',
            'year':datetime.now().year
        }))
    elif request.method == 'POST':
        form = DefectForm(request.POST)
        if form.is_valid():
            defect = Defect(description = form.cleaned_data['description'], resolved_by = form.cleaned_data['resolved_by_DeveloperID'], removediter = form.cleaned_data['removediter'], defect_type = form.cleaned_data['defect_type'], removedphase = form.cleaned_data['removedphase'], injectedphase = form.cleaned_data['injectedphase'], injectediter = form.cleaned_data['injectediter'])
            defect.projectid = project.pid
            defect.byname = Developer.objects.get(pk=defect.resolved_by).name
            defect.save()
            print(defect.description)
        return HttpResponseRedirect('/project/%s' %pid)

def enditeration(request,iterid):
    iteration = Iteration.objects.get(pk=iterid)
    iteration.status = False
    iteration.save()
    print(iteration.projectid)
    return HttpResponseRedirect('/project/analysis/%s' % iteration.projectid)

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

def defect_starttimer(request, iterid):
    iteration = Iteration.objects.get(pk=iterid)
    project = Project.objects.get(pk=iteration.projectid)
    start = datetime.now()
    iteration.defect_laststart = start
    iteration.save()
    return HttpResponseRedirect('/project/iteration/%s/defecttimer' % iterid)

def defect_itertimer(request, iterid):
    iteration = Iteration.objects.get(pk=iterid)
    project = Project.objects.get(pk=iteration.projectid)
    return render_to_response('app/defect_itertimer.html', {'iteration':iteration, 'project':project},
                              context_instance = RequestContext(request,
        {
            'title':'Timer',
            'year':datetime.now().year
        }))

def defect_endtimer(request, iterid):
    iteration = Iteration.objects.get(pk=iterid)
    end = datetime.now()
    start = iteration.defect_laststart
    hour = end.hour - start.hour
    minute = end.minute - start.minute
    sec = end.second - start.second
    iteration.defect_lastend = end
    iteration.defect_timecost += hour*3600 + minute*60 + sec
    iteration.save()
    return HttpResponseRedirect('/project/iteration/%s' % iterid)

def defects(request, pid):
    project = Project.objects.get(pk=pid)
    defects = Defect.objects.filter(projectid=pid)

    return render_to_response('app/defects.html',{'project':project, 'defects':defects},
                              context_instance = RequestContext(request,
        {
            'title':'Viewdefects',
            'year':datetime.now().year
        }))

def manager_login(request):
	c = {}
	c.update(csrf(request))
	return render_to_response('app/manager_login.html', c)

def developer_login(request):
	c = {}
	c.update(csrf(request))
	return render_to_response('app/developer_login.html', c)

def manager_auth_view(request):
    username = request.POST.get('username', '')
    password = request.POST.get('password', '')
    user = authenticate(username=username, password=password)
    if user is not None:
        if user.is_active:
        	request.session['_username'] = username
        	return HttpResponseRedirect('/managerAC')
    else:
    	request.session['_error'] = "invalid username or password"
    	return HttpResponseRedirect('/manager_loginFail')

def developer_auth_view(request):
    username = request.POST.get('username', '')
    password = request.POST.get('password', '')
    user = authenticate(username=username, password=password)
    if user is not None:
        if user.is_active:
        	request.session['_username'] = username
        	return HttpResponseRedirect('/developerAC')
    else:
    	request.session['_error'] = "invalid username or password"
    	return HttpResponseRedirect('/developer_loginFail')

def managerAC(request):
	if request.session.has_key('_username'):
		_username = request.session.get('_username')
		if _username == "manager":
			return HttpResponseRedirect('/manager')
		else:
			request.session['_error'] = "invalid username or password"
			return HttpResponseRedirect('/manager_loginFail')

def developerAC(request):
	if request.session.has_key('_username'):
		_username = request.session.get('_username')
		if _username == "jackie":
			workerid = 2
			return HttpResponseRedirect('/developer/%s' % workerid)
		if _username == "felix":
			workerid = 1
			return HttpResponseRedirect('/developer/%s' % workerid)
		else:
			request.session['_error'] = "invalid username or password"
			return HttpResponseRedirect('/developer_loginFail')

def manager_loginFail(request):
	c = {'error':request.session.get('_error')}
	c.update(csrf(request))
	return render_to_response('app/manager_login.html', c)

def developer_loginFail(request):
	c = {'error':request.session.get('_error')}
	c.update(csrf(request))
	return render_to_response('app/developer_login.html', c)

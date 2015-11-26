"""
Definition of urls for PDT.
"""

from datetime import datetime
from django.conf.urls import patterns, url
from app.forms import BootstrapAuthenticationForm

# Uncomment the next lines to enable the admin:
# from django.conf.urls import include
# from django.contrib import admin
# admin.autodiscover()

urlpatterns = patterns('',
    url(r'^$', 'app.views.home', name='home'),
    #manager pages
    url(r'^manager$', 'app.views.managerhome', name='managerhome'),
    url(r'^project/analysis/(?P<pid>\d+)$', 'app.views.projectanalysis', name='projectanalysis'),
    url(r'^project/edit/(?P<pid>\d+)$', 'app.views.editproject', name='editproject'),
    url(r'^manager/create$', 'app.views.createproject', name='createproject'),
    url(r'^manager/iteration/create$', 'app.views.createiteration', name='createiteration'),
    url(r'^manager/iteration/(?P<iterid>\d+)$', 'app.views.itrdetail', name='itrdetail'),
    #developer pages
    url(r'^developers$','app.views.developers', name='developers'),
    url(r'^developer/(?P<workerid>\d+)$', 'app.views.developerhome', name='developerhome'),
    url(r'^project/(?P<pid>\d+)$', 'app.views.projectdetail', name='projectdetail'),
    url(r'^project/iteration/(?P<iterid>\d+)$', 'app.views.iterationpage', name='iterationpage'),
    url(r'^project/iteration/(?P<iterid>\d+)/starttimer$', 'app.views.startitimer', name='startitimer'),
    url(r'^project/iteration/(?P<iterid>\d+)/timer$', 'app.views.itertimer', name='itertimer'),
    url(r'^project/iteration/(?P<iterid>\d+)/endtimer$', 'app.views.enditimer', name='enditimer'),
    url(r'^login/$',
        'django.contrib.auth.views.login',
        {
            'template_name': 'app/login.html',
            'authentication_form': BootstrapAuthenticationForm,
            'extra_context':
            {
                'title':'Log in',
                'year':datetime.now().year,
            }
        },
        name='login'),
    url(r'^logout$',
        'django.contrib.auth.views.logout',
        {
            'next_page': '/',
        },
        name='logout'),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    # url(r'^admin/', include(admin.site.urls)),
)

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
    url(r'^manager_login$', 'app.views.manager_login', name='_login'),
    url(r'^developer_login$', 'app.views.developer_login', name='_login'),
    url(r'^manager_auth$', 'app.views.manager_auth_view'),
    url(r'^developer_auth$', 'app.views.developer_auth_view'),
    url(r'^managerAC$', 'app.views.managerAC'),
    url(r'^developerAC$', 'app.views.developerAC'),
    url(r'^manager_loginFail$', 'app.views.manager_loginFail'),
    url(r'^developer_loginFail$', 'app.views.developer_loginFail'),
    url(r'^manager$', 'app.views.managerhome', name='managerhome'),
    url(r'^project/analysis/(?P<pid>\d+)$', 'app.views.projectanalysis', name='projectanalysis'),
    url(r'^project/metrics/(?P<pid>\d+)$', 'app.views.metrics', name='projectmetrics'),
    url(r'^project/metrics/(?P<pid>\d+)/defects$', 'app.views.defects', name='projectdefects'),
    url(r'^project/edit/(?P<pid>\d+)$', 'app.views.editproject', name='editproject'),
    url(r'^manager/create$', 'app.views.createproject', name='createproject'),
    url(r'^manager/iteration/create/(?P<pid>\d+)$', 'app.views.createiteration', name='createiteration'),
    url(r'^manager/iteration/(?P<iterid>\d+)$', 'app.views.itrdetail', name='itrdetail'),
    url(r'^manager/iteration/timer/(?P<iterid>\d+)$', 'app.views.changetime', name='changetime'),
    #developer pages
    url(r'^developers$','app.views.developers', name='developers'),
    url(r'^developer/(?P<workerid>\d+)$', 'app.views.developerhome', name='developerhome'),
    url(r'^project/(?P<pid>\d+)$', 'app.views.projectdetail', name='projectdetail'),
    url(r'^project/iteration/(?P<iterid>\d+)$', 'app.views.iterationpage', name='iterationpage'),
    url(r'^project/iteration/(?P<iterid>\d+)/starttimer$', 'app.views.startitimer', name='startitimer'),
    url(r'^project/iteration/(?P<iterid>\d+)/timer$', 'app.views.itertimer', name='itertimer'),
    url(r'^project/iteration/(?P<iterid>\d+)/endtimer$', 'app.views.enditimer', name='enditimer'),
    url(r'^project/iteration/(?P<iterid>\d+)/startdefecttimer$', 'app.views.defect_starttimer', name='defect_starttimer'),
    url(r'^project/iteration/(?P<iterid>\d+)/defecttimer$', 'app.views.defect_itertimer', name='defect_itertimer'),
    url(r'^project/iteration/(?P<iterid>\d+)/enddefecttimer$', 'app.views.defect_endtimer', name='defect_endtimer'),
    url(r'^project/iteration/(?P<iterid>\d+)/enditeration$', 'app.views.enditeration', name='enditeration'),
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

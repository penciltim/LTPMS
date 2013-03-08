from contact.views import *
from django.conf import settings
from django.conf.urls import patterns, include, url
from django.contrib import admin
from django.contrib.auth.views import login, logout
from project.views import *

# Uncomment the next two lines to enable the admin:
admin.autodiscover()

urlpatterns = patterns('',
    url(r'^$', home),
    url(r'^display_meta/$', display_meta),
    url(r'^contactus/$', contact),
    url(r'^admin/', include(admin.site.urls)),
)


urlpatterns += patterns('project.views',
    url(r'^project/$', 'project_list'),
    url(r'^project/add/$', 'project_add'),
    url(r'^project/(\d+)/edit/$', 'project_edit'),
    url(r'^project/(\d+)/delete/$', 'project_delete'),
    url(r'^purchase/$', 'purchase'),
    url(r'^about/$', 'about'),
    
    (r'^accounts/login/$', login),
    (r'^accounts/logout/$', logout),
)

urlpatterns += patterns('weeklyreport.views',
    url(r'^weeklyreport/$', 'weeklyreport_list'),
    url(r'^weeklyreport/add/$', 'weeklyreport_add'),
    url(r'^weeklyreport/(\d+)/edit/$', 'weeklyreport_edit'),
    url(r'^weeklyreport/(\d+)/delete/$', 'weeklyreport_delete'),
)

if settings.DEBUG:
    urlpatterns += patterns('',
            url(r"^uploads/(?P<path>.*)$", \
                "django.views.static.serve", \
                {"document_root": settings.MEDIA_ROOT, }),
)

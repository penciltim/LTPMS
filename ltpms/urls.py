from django.conf.urls import patterns, include, url
from project.views import *
from contact.views import *
from django.contrib.auth.views import login, logout

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    url(r'^$', base_site),
    url(r'^display_meta/$', display_meta),
    url(r'^contactus/$', contact),
    url(r'^admin/', include(admin.site.urls)),
)


urlpatterns += patterns('project.views',
    url(r'^project/$', 'project_list'),
    url(r'^project/add/$', 'project_add'),
    url(r'^project/(\d+)/edit/$', 'project_edit'),
    url(r'^project/(\d+)/$', 'project_view'),
    url(r'^project/(\d+)/delete/$', 'project_delete'),
    url(r'^project/(\d+)/update/$', 'project_update'),
    url(r'^purchase/$', 'purchase'),
    url(r'^test/$', 'test'),
    (r'^accounts/login/$',  login),
    (r'^accounts/logout/$', logout),
)
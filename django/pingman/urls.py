from django.conf.urls import patterns, include, url
from splunkdj.utility.views import render_template as render

urlpatterns = patterns('',
    url(r'^home/$', 'pingman.views.home', name='home'), 
    url(r'^dashboard/$', 'pingman.views.dashboard', name='dashboard'), 
    url(r'^alert/$', 'pingman.views.alert', name='alert'), 
 )

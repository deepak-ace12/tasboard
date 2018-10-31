from django.conf.urls import url
from django.contrib.auth.views import login, logout

from todo import views

urlpatterns = [
    url(r'^home/$', views.home, name='home'),
    url(r'^home/(?P<status>.+)/$', views.home, name='filter'),
    url(r'^login/$',
        login, {'template_name': 'todo/login.html'}, name='login'),
    url(r'^logout/$',
        logout, {'template_name': 'todo/logout.html'}, name='logout'),
    url(r'^register/$', views.register, name='register'),
    url(r'^task/create/$', views.add_or_update_task, name='add_task'),
    url(r'^task/(?P<pk>\d+)/update/$',
        views.add_or_update_task, name='update_task'),
    url(r'^pending/$', views.pending_requests, name='pending_requests'),
    url(r'^approve/(?P<pk>\d+)/$',
        views.approve_request, name='approve_request'),
]

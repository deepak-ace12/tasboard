from django.conf.urls import url, include
from django.contrib import admin
from .views import login_redirect


urlpatterns = [
    url(r'^$', login_redirect, name='login_redirect'),
    url(r'^admin/', admin.site.urls),
    url(r'^todo/', include('todo.urls',  namespace='todo')),
]

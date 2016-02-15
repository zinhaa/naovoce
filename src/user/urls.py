from django.conf.urls import url

from . import views as user


urlpatterns = [
    url(r'^index/$', user.index, name='index'),
    url(r'^(?P<pk>\d+)(?:-(?P<slug>[^/]+))?/$', user.profile, name='detail'),
]

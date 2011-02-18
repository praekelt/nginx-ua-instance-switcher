from django.conf.urls.defaults import *

urlpatterns = patterns('',
    url(r'^map-request/$', 'ua_mapper.views.map_request', name='map_request'),
)

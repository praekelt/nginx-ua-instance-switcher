from django.conf.urls.defaults import patterns, include

urlpatterns = patterns(
    '',
    (r'^$', 'project.views.home'),
    (r'^mapper/', include('ua_mapper.urls')),
)

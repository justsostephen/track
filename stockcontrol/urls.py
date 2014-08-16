from django.conf.urls import patterns, include, url

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'stockcontrol.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^lending/', include('lending.urls', namespace="lending")),
    url(r'^registration/', include(
        'registration.urls', namespace="registration")),
    url(r'^admin/', include(admin.site.urls)),
)

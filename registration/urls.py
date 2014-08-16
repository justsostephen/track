from django.conf.urls import patterns, url

from registration import views

urlpatterns = patterns('',
    url(r'^$', views.issue_item, name='issue_item'),
    url(r'^issue/$', views.issue_item, name='issue_item'),
    url(r'^issue/(\d+)/$', views.issue_item, name='issue_item'),
    url(r'^return/$', views.return_item, name='return_item'),
    url(r'^return/(\d+)/$', views.return_item, name='return_item'),
)

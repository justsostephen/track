from django.conf.urls import patterns, url

from lending import views

urlpatterns = patterns('',
    url(r'^$', views.borrow_item, name='borrow_item'),
    url(r'^users/$', views.UserList.as_view(), name='users'),
    url(r'^user/(?P<pk>\d+)/$', views.UserDetail.as_view(), name='user'),
    url(r'^items/$', views.ItemList.as_view(), name='items'),
    url(r'^history/$', views.HistoryList.as_view(), name='history'),
    url(r'^tablets/$', views.TabletList.as_view(), name='tablets'),
    url(r'^tablet/(?P<pk>\d+)/$', views.TabletDetail.as_view(), name='tablet'),
    url(r'^lent/$', views.LentList.as_view(), name='lent'),
    url(r'^borrow/$', views.borrow_item, name='borrow_item'),
    url(r'^borrow/(\d+)/$', views.borrow_item, name='borrow_item'),
    url(r'^return/$', views.return_item, name='return_item'),
    url(r'^return/(\d+)/$', views.return_item, name='return_item'),
    url(r'^bugs_features/$', views.submit_bug_feature,
        name='submit_bug_feature'),
)

from django.conf.urls import include, url

from .views import MembershipApplicationAddView, MembershipApplicationDetailView, MembershipApplicationListView

app_name = 'application'
urlpatterns = [
    url(r'^view/(?P<view_link_key>[^//]+)/$', MembershipApplicationDetailView.as_view(lookup_field='view_link_key'),
        name='application-view'),
    url(r'^list/$', MembershipApplicationListView.as_view(), name='application-list'),
    url(r'^$', MembershipApplicationAddView.as_view(), name='application-add'),
]

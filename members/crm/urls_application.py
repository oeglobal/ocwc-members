from django.conf.urls import patterns, include, url

from .views import MembershipApplicationAddView, MembershipApplicationDetailView

urlpatterns = patterns('',
	url(r'^view/(?P<view_link_key>[^//]+)/$', MembershipApplicationDetailView.as_view(lookup_field='view_link_key'), name='application-view'),
	url(r'^$', MembershipApplicationAddView.as_view(), name='application-add'),
)
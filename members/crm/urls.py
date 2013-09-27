from django.conf.urls import patterns, url

from .views import OrganizationIndex, OrganizationDetailView, OrganizationEdit

urlpatterns = patterns('',
	url(r'^member/view/(?P<pk>\d+)/$', OrganizationDetailView.as_view(), name='organization-view'),
	url(r'^member/edit/(?P<pk>\d+)/$', OrganizationEdit.as_view(), name='organization-edit'),

	url(r'^$', OrganizationIndex.as_view(), name='index'),
)
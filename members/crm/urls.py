from django.conf.urls import patterns, url

from .views import OrganizationIndex, OrganizationDetailView, OrganizationEdit, \
	ReportedStatisticDetailView, ReportedStatisticEditView, ReportedStatisticAddView

urlpatterns = patterns('',
	url(r'^member/view/(?P<pk>\d+)/$', OrganizationDetailView.as_view(), name='organization-view'),
	url(r'^member/edit/(?P<pk>\d+)/$', OrganizationEdit.as_view(), name='organization-edit'),

	url(r'^member/statistics/view/(?P<pk>\d+)/$', ReportedStatisticDetailView.as_view(), name='reported-statistics-view'),
	url(r'^member/statistics/edit/(?P<pk>\d+)/$', ReportedStatisticEditView.as_view(), name='reported-statistics-edit'),
	url(r'^member/statistics/add/(?P<pk>\d+)/$', ReportedStatisticAddView.as_view(), name='reported-statistics-add'),
	url(r'^$', OrganizationIndex.as_view(), name='index'),
)
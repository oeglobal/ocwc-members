from django.conf.urls import patterns, include, url

from .views import MembershipApplicationAddView

urlpatterns = patterns('',
	url(r'^$', MembershipApplicationAddView.as_view(), name='application_add'),
)
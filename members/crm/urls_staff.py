from django.conf.urls import patterns, url

from .views import StaffIndex, OrganizationStaffView, OrganizationStaffListView, OrganizationStaffDetailView, \
				   InvoiceStaffView, InvoicePhantomJSView, BillingLogCreateView, OrganizationBillingLogListingView

# namespace='staff', app_name='crm'

urlpatterns = patterns('',
	url(r'^$', StaffIndex.as_view(), name='index'),

	url(r'^invoice/view/(?P<pk>\d+)/$', InvoiceStaffView.as_view(), name='invoice-view'),
	url(r'^invoice/key/(?P<access_key>\w+)/$', InvoicePhantomJSView.as_view(lookup_field='access_key'), name='invoice-phantomjs-view'),
	# url(r'^invoice/create/$', InvoiceCreateView.as_view(), name='invoice-create'),

	url(r'^billinglog/create/$', BillingLogCreateView.as_view(), name='billinglog-create'),
	url(r'^billinglog/list/(?P<username>\w+)/$', OrganizationBillingLogListingView.as_view(), name='billinglog-username-listing'),

    url(r'^organization/view/(?P<pk>\d+)/$', OrganizationStaffDetailView.as_view(), name='organization-view'),
    url(r'^organization/list/$', OrganizationStaffListView.as_view(), name='organization-list'),
)

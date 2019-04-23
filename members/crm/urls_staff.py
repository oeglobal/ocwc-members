from django.conf.urls import url

from .views import (
    StaffIndex,
    OrganizationStaffListView,
    OrganizationStaffDetailView,
    InvoiceStaffView,
    InvoicePhantomJSView,
    BillingLogCreateView,
    OrganizationBillingLogListingView,
    OrganizationExportExcel,
    OrganizationStaffNoContactListView,
    OrganizationStaffCccOerListView,
    OrganizationExportCccoerExcel,
    QuickBooksLogin,
)

app_name = "staff"
urlpatterns = [
    url(r"^$", StaffIndex.as_view(), name="index"),
    url(
        r"^invoice/view/(?P<pk>\d+)/$", InvoiceStaffView.as_view(), name="invoice-view"
    ),
    url(
        r"^invoice/key/(?P<access_key>\w+)/$",
        InvoicePhantomJSView.as_view(lookup_field="access_key"),
        name="invoice-phantomjs-view",
    ),
    # url(r'^invoice/create/$', InvoiceCreateView.as_view(), name='invoice-create'),
    url(
        r"^billinglog/create/$",
        BillingLogCreateView.as_view(),
        name="billinglog-create",
    ),
    url(
        r"^billinglog/list/(?P<username>\w+)/$",
        OrganizationBillingLogListingView.as_view(),
        name="billinglog-username-listing",
    ),
    url(
        r"^organization/view/(?P<pk>\d+)/$",
        OrganizationStaffDetailView.as_view(),
        name="organization-view",
    ),
    url(
        r"^organization/list/excel/$",
        OrganizationExportExcel.as_view(),
        name="organization-list-excel",
    ),
    url(
        r"^organization/list/excel-cccoer/$",
        OrganizationExportCccoerExcel.as_view(),
        name="organization-list-excel-cccoer",
    ),
    url(
        r"^organization/list/nocontact/$",
        OrganizationStaffNoContactListView.as_view(),
        name="organization-list-nocontact",
    ),
    url(
        r"^organization/list/cccoer/$",
        OrganizationStaffCccOerListView.as_view(),
        name="organization-list-cccoer",
    ),
    url(
        r"^organization/list/$",
        OrganizationStaffListView.as_view(),
        name="organization-list",
    ),
    url(r"^quickbooks/$", QuickBooksLogin.as_view(), name="quickbooks"),
]

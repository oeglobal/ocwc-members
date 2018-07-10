from django.conf.urls import url

from .views import ConferenceIndex, InvoicePDF, InvoicePreview, PingInvoices

app_name = 'conferences'
urlpatterns = [
    url(r'^$', ConferenceIndex.as_view(), name='index'),

    url(r'^invoice/ping/$', PingInvoices.as_view(), name='invoice_ping'),

    url(r'^invoice/(?P<pk>\d+)/$', InvoicePDF.as_view(), name='invoice_download'),
    url(r'^invoice/(?P<pk>\d+)/(?P<access_key>\w+)/$', InvoicePreview.as_view(), name='invoice_preview'),
]

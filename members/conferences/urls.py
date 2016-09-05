from django.conf.urls import patterns, url

from .views import ConferenceIndex, InvoicePDF, InvoicePreview

urlpatterns = patterns('',
    url(r'^$', ConferenceIndex.as_view(), name='index'),

    url(r'^invoice/(?P<pk>\d+)/$', InvoicePDF.as_view(), name='invoice_download'),
    url(r'^invoice/(?P<pk>\d+)/(?P<access_key>\w+)/$', InvoicePreview.as_view(), name='invoice_preview'),
)

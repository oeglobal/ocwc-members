# -*- coding: utf-8 -*-
from django.shortcuts import redirect
from django.contrib import messages
from django.conf import settings
from django.http import HttpResponse

from vanilla import TemplateView
from braces.views import StaffuserRequiredMixin

from rest_framework.views import APIView
from rest_framework.response import Response

from crm.utils import print_pdf

from .models import ConferenceRegistration
from .utils import sync_conference


class ConferenceIndex(StaffuserRequiredMixin, TemplateView):
    template_name = 'conferences/index.html'

    def post(self, request):
        messages.success(self.request, 'Conference registrations synced')
        return redirect('conferences:index')

    def get_context_data(self, *args, **kwargs):
        ctx = super(ConferenceIndex, self).get_context_data(*args, **kwargs)
        ctx['registration_list'] = ConferenceRegistration.objects.filter(interface=2)

        return ctx


class InvoicePDF(StaffuserRequiredMixin, TemplateView):
    def get(self, request, pk=None):
        registration = ConferenceRegistration.objects.get(
                            pk=self.kwargs.get('pk'))

        paid_queryparam = ''
        if request.GET.get('paid'):
            paid_queryparam = '?paid=1'

        url = '{}{}{}'.format(settings.INVOICES_PHANTOM_JS_HOST, registration.get_access_key_url(), paid_queryparam)

        pdf_file = print_pdf(url)

        response = HttpResponse(pdf_file, content_type='application/pdf')
        response['Content-Disposition'] = 'inline;filename=OEGlobal-Invoice-{}.pdf'.format(registration.entry_id)
        return response


class InvoicePreview(TemplateView):
    template_name = 'conferences/invoice.html'

    def get_context_data(self, *args, **kwargs):
        ctx = super(InvoicePreview, self).get_context_data(*args, **kwargs)

        registration = ConferenceRegistration.objects.get(
                            pk=self.kwargs.get('pk'),
                            access_key=self.kwargs.get('access_key')
                        )
        ctx['invoice'] = registration

        if self.request.GET.get('paid'):
            ctx['paid'] = True

        return ctx


class PingInvoices(APIView):
    def get(self, request, format=None):
        sync_conference()

        return Response('OK')

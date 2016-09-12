# -*- coding: utf-8 -*-
import os
import uuid
import subprocess

from django.shortcuts import redirect
from django.contrib import messages
from django.conf import settings
from django.http import HttpResponse

from vanilla import TemplateView
from braces.views import StaffuserRequiredMixin

from .models import ConferenceRegistration

here = lambda x: os.path.join(os.path.dirname(os.path.abspath(__file__)), x)

class ConferenceIndex(StaffuserRequiredMixin, TemplateView):
    template_name = 'conferences/index.html'

    def post(self, request):
        messages.success(self.request, 'Conference registrations synced')
        return redirect('conferences:index')

    def get_context_data(self, *args, **kwargs):
        ctx = super(ConferenceIndex, self).get_context_data(*args, **kwargs)
        ctx['registration_list'] = ConferenceRegistration.objects.all()

        return ctx

class InvoicePDF(StaffuserRequiredMixin, TemplateView):
    def get(self, request, pk=None):
        registration = ConferenceRegistration.objects.get(
                            pk=self.kwargs.get('pk'))

        url = '%s%s' % (settings.INVOICES_PHANTOM_JS_HOST, registration.get_access_key_url())

        pdf = '/tmp/oeglobal_invoice_{}.pdf'.format(uuid.uuid4().get_hex())
        popen_instance = subprocess.Popen([here('../../bin/phantomjs'),
                          here('../crm/phantomjs-scripts/rasterize.js'),
                          url,
                          pdf,
                          'Letter'
                        ])

        subprocess.Popen.wait(popen_instance)

        with open(pdf, 'r') as pdf_file:
            response = HttpResponse(pdf_file.read(), mimetype='application/pdf')
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

        ctx['ticket_type'] = registration.ticket_type.split('|')[0]
        ctx['ticket_price'] = registration.ticket_type.split('|')[1]

        dinner_ticket = registration.dinner_guest.split('|')[0]
        if dinner_ticket == 'Yes':
            ctx['dinner_ticket'] = True
            ctx['dinner_price'] = registration.dinner_guest.split('|')[1]

        return ctx

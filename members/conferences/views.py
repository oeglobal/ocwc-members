from django.core.mail import send_mail
from django.shortcuts import redirect, render
from django.contrib import messages
from django.conf import settings
from django.http import HttpResponse
from django.db.models import Q

from vanilla import TemplateView, FormView
from braces.views import StaffuserRequiredMixin

from rest_framework.views import APIView
from rest_framework.response import Response

from crm.utils import print_pdf
from .forms import ConnectForm

from .models import (
    ConferenceRegistration,
    ConferenceEmailLogs,
    ConferenceEmailRegistration,
    ConferenceEmailTemplate,
)
from .utils import sync_conference


class ConferenceIndex(StaffuserRequiredMixin, TemplateView):
    template_name = "conferences/index.html"

    def post(self, request):
        messages.success(self.request, "Conference registrations synced")
        return redirect("conferences:index")

    def get_context_data(self, *args, **kwargs):
        ctx = super(ConferenceIndex, self).get_context_data(*args, **kwargs)

        q = self.request.GET.get("q")
        queryset = ConferenceRegistration.objects.filter(interface=2)
        if q:
            ctx["q"] = q
            queryset = queryset.filter(
                Q(name__icontains=q)
                | Q(organization__icontains=q)
                | Q(billing_html__icontains=q)
            )
        else:
            queryset = ConferenceRegistration.objects.filter(interface=2)

        ctx["registration_list"] = queryset

        return ctx


class InvoicePDF(StaffuserRequiredMixin, TemplateView):
    def get(self, request, pk=None):
        registration = ConferenceRegistration.objects.get(pk=self.kwargs.get("pk"))

        paid_queryparam = ""
        if request.GET.get("paid"):
            paid_queryparam = "?paid=1"

        url = "{}{}{}".format(
            settings.INVOICES_PHANTOM_JS_HOST,
            registration.get_access_key_url(),
            paid_queryparam,
        )

        pdf_file = print_pdf(url)

        response = HttpResponse(pdf_file, content_type="application/pdf")
        response[
            "Content-Disposition"
        ] = "inline;filename=OEGlobal-Invoice-{}.pdf".format(registration.entry_id)
        return response


class InvoicePreview(TemplateView):
    template_name = "conferences/invoice.html"

    def get_context_data(self, *args, **kwargs):
        ctx = super(InvoicePreview, self).get_context_data(*args, **kwargs)

        registration = ConferenceRegistration.objects.get(
            pk=self.kwargs.get("pk"), access_key=self.kwargs.get("access_key")
        )
        ctx["invoice"] = registration

        if self.request.GET.get("paid"):
            ctx["paid"] = True

        return ctx


class PingInvoices(APIView):
    def get(self, request, format=None):
        sync_conference()

        return Response("OK")


class ConnectEmail(FormView):
    template_name = "conferences/email_form.html"
    form_class = ConnectForm

    def form_valid(self, form):
        email = form.cleaned_data["email"]
        reg = ConferenceEmailRegistration.objects.get(email__iexact=email)
        ConferenceEmailLogs.objects.create(action=str(reg))

        template = ConferenceEmailTemplate.objects.get(email_type=reg.email_type)
        send_mail(
            template.subject,
            template.body_text,
            "conference@oeglobal.org",
            [email],
            html_message=template.body_html,
        )

        return render(
            self.request, "conferences/email_form-done.html", {"email": email}
        )

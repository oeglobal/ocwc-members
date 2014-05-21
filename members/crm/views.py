# -*- coding: utf-8 -*-
import collections
import datetime
import xlwt

from django import forms
from django.http import Http404, HttpResponse
from django.conf import settings
from django.shortcuts import render, redirect
from django.contrib.auth import login
from django.core.urlresolvers import reverse
from django.template.loader import render_to_string

from vanilla import ListView, DetailView, TemplateView, UpdateView, CreateView, FormView
from braces.views import LoginRequiredMixin, StaffuserRequiredMixin

from rest_framework.response import Response
from rest_framework.decorators import api_view, renderer_classes
from rest_framework import generics
from rest_framework.renderers import JSONRenderer, JSONPRenderer, BrowsableAPIRenderer
from rest_framework.authentication import SessionAuthentication, BasicAuthentication
from rest_framework.permissions import IsAuthenticated

from .models import Organization, Contact, Address, ReportedStatistic, Country, MembershipApplication, \
    LoginKey, Invoice, BillingLog
from .serializers import OrganizationApiSerializer, OrganizationDetailedApiSerializer, OrganizationRssFeedsApiSerializer
from .forms import MembershipApplicationModelForm, MemberLoginForm, AddressModelForm, BillingLogForm, ReportedStatisticModelForm


class IndexView(FormView):
    template_name = 'index.html'
    form_class = MemberLoginForm

    def form_valid(self, form):
        get = form.cleaned_data.get
        org = Organization.objects.get(pk=get('organization'))
        email = get('email')

        ctx = {
            'email': email
        }

        key = LoginKey(user=org.user, email=email)
        key.save()
        key.send_email()

        return render(self.request, 'mail-login/mail_sent.html', ctx)

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_staff:
            return redirect('/staff/')
        elif request.user.is_authenticated():
            return redirect('/crm/')

        return super(IndexView, self).dispatch(request, *args, **kwargs)


class OrganizationView(LoginRequiredMixin):
    pass


class OrganizationIndex(OrganizationView, DetailView):
    model = Organization
    template_name = 'overview_index.html'
    context_object_name = 'org'

    def get_object(self):
        return self.request.user.organization_set.latest('id')


class OrganizationDetailView(OrganizationView, DetailView):
    model = Organization
    template_name = "organization_detail.html"
    context_object_name = "org"


class OrganizationStaffModelForm(forms.ModelForm):
    class Meta:
        model = Organization
        fields = ['membership_type', 'membership_status', 'associate_consortium',
                  'display_name', 'legal_name', 'main_website', 'ocw_website', 'description',
                  'logo_large', 'logo_small', 'rss_course_feed']


class OrganizationModelForm(forms.ModelForm):
    class Meta:
        model = Organization
        fields = ['display_name', 'main_website', 'ocw_website', 'description',
                  'logo_large', 'logo_small', 'rss_course_feed']


class OrganizationEdit(OrganizationView, UpdateView):
    model = Organization
    template_name = 'organization_edit.html'

    def get_form_class(self):
        if self.request.user.is_staff:
            return OrganizationStaffModelForm
        return OrganizationModelForm


class AddressEditView(OrganizationView, UpdateView):
    model = Address
    template_name = 'address_edit.html'
    form_class = AddressModelForm

    def get_queryset(self):
        queryset = Address.objects.filter(pk=self.kwargs.get('pk'))
        if self.request.user.is_staff:
            return queryset

        return queryset.filter(organization__user=self.request.user)


class ReportedStatisticDetailView(OrganizationView, DetailView):
    model = ReportedStatistic
    template_name = 'reported_statistic_view.html'
    context_object_name = 'statistic_list'

    def get_object(self):
        org = Organization.objects.get(pk=self.kwargs['pk'])
        return ReportedStatistic.objects.filter(organization=org).order_by('report_date')


class ReportedStatisticEditView(OrganizationView, UpdateView):
    model = ReportedStatistic
    template_name = 'reported_statistic_edit.html'
    context_object_name = 'stat'
    form_class = ReportedStatisticModelForm


class ReportedStatisticAddView(CreateView):
    model = ReportedStatistic
    template_name = 'reported_statistic_add.html'
    context_object_name = 'stat'
    form_class = ReportedStatisticModelForm

    def get_form(self, data=None, files=None, **kwargs):
        org = Organization.objects.get(pk=self.kwargs['pk'])
        if not (self.request.user.is_staff or self.request.user == org.user):
            raise Http404

        kwargs['organization'] = org
        return self.get_form_class()(data, files, **kwargs)


class MembershipApplicationAddView(CreateView):
    model = MembershipApplication
    template_name = 'membership_application_add.html'
    context_object_name = 'application'
    form_class = MembershipApplicationModelForm


class MembershipApplicationDetailView(DetailView):
    model = MembershipApplication
    template_name = 'membership_application_view.html'
    context_object_name = 'app'

    # def get_object(self):
    #   return MembershipApplication.objects.get(view_link_key=self.kwargs['view_link_key'])


class MembershipApplicationListView(StaffuserRequiredMixin, ListView):
    model = MembershipApplication
    template_name = 'membership_application_list.html'

    def get_queryset(self):
        return self.model.objects.all().order_by('-id')[:25]


### Staff specific views
class StaffView(LoginRequiredMixin, StaffuserRequiredMixin):
    pass


class StaffIndex(StaffView, TemplateView):
    template_name = 'staff/index.html'


class OrganizationStaffView(StaffView):
    model = Organization


class OrganizationStaffListView(OrganizationStaffView, ListView):
    template_name = 'staff/organization_list.html'

    def get_queryset(self):
        return self.model.objects.filter(membership_status__in=(2, 3, 4, 5, 7, 99)).order_by('display_name')


class OrganizationStaffDetailView(OrganizationStaffView, DetailView):
    template_name = 'staff/organization_detail.html'
    context_object_name = 'org'

    def get_context_data(self, **kwargs):
        context = super(OrganizationStaffDetailView, self).get_context_data(**kwargs)

        try:
            lead_contact = self.object.contact_set.filter(contact_type=6).latest('id')
            first_name = lead_contact.first_name
            email = lead_contact.email
        except (Contact.DoesNotExist):
            first_name = ''
            email = ''

        email_invoice_subject = '%s OCW Consortium Membership invoice' % settings.DEFAULT_INVOICE_YEAR
        email_invoice_body = render_to_string('staff/invoice_mail.txt', {'first_name': first_name, 'user': self.request.user})

        email_invoice_paid_subject = '%s OCW Consortium Membership payment receipt' % settings.DEFAULT_INVOICE_YEAR
        email_invoice_paid_body = render_to_string('staff/invoice_paid_mail.txt', {'first_name': first_name, 'user': self.request.user})

        initial = {
            'organization': self.object.id,
            'user': self.request.user.id,
            'amount': self.object.get_membership_due_amount(),
            'invoice_year': settings.DEFAULT_INVOICE_YEAR,
            'first_name': first_name,
            'email_invoice': email,
            'email_invoice_subject': email_invoice_subject,
            'email_invoice_body': email_invoice_body,
            'email_invoice_paid': email,
            'email_invoice_paid_subject': email_invoice_paid_subject,
            'email_invoice_paid_body': email_invoice_paid_body,
            'description': 'OpenCourseWare Consortium %s Membership' % settings.DEFAULT_INVOICE_YEAR
        }

        try:
            log = self.object.billinglog_set.filter(invoice_year=settings.DEFAULT_INVOICE_YEAR,
                                                    log_type='create_invoice').latest('id')
            initial.update({
                'amount': log.invoice.amount,
                'description': log.invoice.description
            })
        except BillingLog.DoesNotExist:
            pass

        context['form'] = BillingLogForm(initial=initial)
        return context


class InvoiceStaffView(StaffView, DetailView):
    model = Invoice
    template_name = 'staff/invoice_detail.html'
    context_object_name = 'invoice'


class InvoicePhantomJSView(DetailView):
    model = Invoice
    template_name = 'staff/invoice_detail.html'
    context_object_name = 'invoice'


class BillingLogCreateView(StaffView, CreateView):
    model = BillingLog
    form_class = BillingLogForm
    template_name = 'staff/billinglog_form.html'

    def form_valid(self, form):
        get = form.cleaned_data.get
        org = get('organization')

        if get('log_type') == 'create_invoice':
            invoice = Invoice(
                invoice_type='issued',
                organization=org,
                invoice_number="%s-%s" % (org.id, get('invoice_year')),
                invoice_year=get('invoice_year'),
                description=get('description'),
                amount=get('amount'),
            )
            invoice.save()

            billing_log = BillingLog(
                log_type='create_invoice',
                organization=get('organization'),
                user=get('user'),
                amount=get('amount'),
                description=get('description'),
                invoice_year=get('invoice_year'),
                invoice=invoice
            )
            billing_log.save()
            invoice.generate_pdf()
        elif get('log_type') == 'create_paid_invoice':
            invoice = Invoice(
                invoice_type='paid',
                organization=org,
                invoice_number="%s-%s" % (org.id, get('invoice_year')),
                invoice_year=get('invoice_year'),
                amount=get('amount'),
                description=get('description'),
            )
            invoice.save()

            billing_log = BillingLog(
                log_type='create_paid_invoice',
                organization=get('organization'),
                user=get('user'),
                amount=get('amount'),
                description=get('description'),
                invoice=invoice,
                invoice_year=get('invoice_year'),
            )
            billing_log.save()
            invoice.generate_pdf()
        elif get('log_type') == 'send_invoice':
            billing_log = BillingLog(
                log_type='send_invoice',
                organization=get('organization'),
                user=get('user'),
                email=get('email_invoice', ''),
                email_subject=get('email_invoice_subject', ''),
                email_body=get('email_invoice_body', ''),
                invoice=Invoice.objects.filter(organization=org, invoice_type='issued').latest('id')
            )
            billing_log.save()
            billing_log.send_email()

        elif get('log_type') == 'send_paid_invoice':
            billing_log = BillingLog(
                log_type='send_paid_invoice',
                organization=get('organization'),
                user=get('user'),
                email=get('email_invoice_paid', ''),
                email_subject=get('email_invoice_paid_subject', ''),
                email_body=get('email_invoice_paid_body', ''),
                invoice=Invoice.objects.filter(organization=org, invoice_type='paid').latest('id')
            )
            billing_log.save()
            billing_log.send_email()
        elif get('log_type') == 'create_note':
            billing_log = BillingLog(
                log_type='create_note',
                organization=get('organization'),
                user=get('user'),
                note=get('note')
            )
            billing_log.save()

        return redirect(reverse('staff:organization-view', kwargs={'pk': org.id}))


class OrganizationBillingLogListingView(StaffView, ListView):
    model = Organization
    template_name = 'staff/billinglog_listing.html'

    def get_queryset(self):
        username = self.kwargs.pop('username')
        return self.model.objects.filter(membership_status__in=(2, 3, 4, 5, 7, 99), ocw_contact__username=username).order_by('display_name')


class OrganizationExportExcel(StaffView, TemplateView):

    def get(self, request, *args, **kwargs):
        response = HttpResponse(mimetype='application/ms-excel')
        response['Content-Disposition'] = 'attachment; filename=members.xls'
        wb = xlwt.Workbook(encoding='utf-8')
        ws = wb.add_sheet("Members")

        row_num = 0
        columns = [
            (u"ID", 25),
            (u"Old ID", 25),
            (u"Name", 150),
            (u"Lead Contact", 70),
            (u"Lead Contact Email", 120),
            (u"Membership status", 70),
            (u"Edit link", 150)
        ]

        font_style = xlwt.XFStyle()
        font_style.font.bold = True

        for col_num in xrange(len(columns)):
            ws.write(row_num, col_num, columns[col_num][0], font_style)
            ws.col(col_num).width = columns[col_num][1] * 100

        font_style = xlwt.XFStyle()
        font_style.alignment.wrap = 1

        for obj in Organization.objects.filter(membership_status__in=(2, 3, 5, 7)).order_by('display_name'):
            row_num += 1

            contact = obj.contact_set.filter(contact_type=6)[0]

            row = [
                obj.pk,
                obj.crmid or '',
                obj.display_name,
                u"%s %s" % (contact.first_name, contact.last_name),
                contact.email,
                obj.get_membership_status_display(),
                'http://members.ocwconsortium.org%s' % obj.get_absolute_staff_url()
            ]

            for col_num in xrange(len(row)):
                ws.write(row_num, col_num, row[col_num], font_style)

        wb.save(response)
        return response


### API views
@api_view(['GET'])
@renderer_classes([BrowsableAPIRenderer, JSONRenderer, JSONPRenderer])
def address_geo_list_view(request):
    features_list = []

    seen_organizations = []
    for address in Address.objects.filter(latitude__isnull=False,
                                          organization__membership_status__in=(2, 3, 5, 7)).select_related():

        org_id = address.organization.id
        if org_id in seen_organizations:
            continue
        else:
            seen_organizations.append(address.organization.id)

        point = {
            "type": "Feature",
            "id": address.organization.id,
            "properties": {
                "name": address.organization.display_name
            },
            "geometry": {
                "type": "Point",
                "coordinates": [address.longitude, address.latitude],
            }
        }
        features_list.append(point)

    data = {
        "type": "FeatureCollection",
        "features": features_list
    }

    return Response(data)


@api_view(['GET'])
def country_list_view(request):
    """
    List available countries for filtering
    """
    data_list = Address.objects.filter(country__isnull=False, organization__membership_status__in=(2, 3, 5, 7)) \
        .order_by('country') \
        .values_list('country', flat=True) \
        .distinct()
    data = Country.objects.filter(pk__in=data_list).order_by('name').values_list('name', flat=True)

    return Response(data)


class OrganizationByCountryListViewApi(generics.ListAPIView):
    serializer_class = OrganizationApiSerializer

    def get_queryset(self):
        organization_list = Address.objects.filter(country__name=self.kwargs.get('country'),
                                                   organization__membership_status__in=(2, 3, 5, 7)).values_list('organization', flat=True).distinct()

        return Organization.objects.filter(pk__in=organization_list).order_by('display_name')


@api_view(['GET'])
def organization_group_by_membership_view(request):
    data = collections.OrderedDict([
        ('Institutions of Higher Education', OrganizationApiSerializer(Organization.active.filter(membership_type__in=(5, 10, 11, 12, 9, 17)), many=True).data),
        ('Associate Consortia', OrganizationApiSerializer(Organization.active.filter(membership_type__in=(7, 14)), many=True).data),
        ('Organizational Members', OrganizationApiSerializer(Organization.active.filter(membership_type__in=(6, 13)), many=True).data),
        ('Corporate Members', OrganizationApiSerializer(Organization.active.filter(membership_type__in=(8, 15, 16)), many=True).data),
    ])

    return Response(data)


class OrganizationViewApi(generics.RetrieveAPIView):
    queryset = Organization.active.all()
    serializer_class = OrganizationDetailedApiSerializer


class OrganizationRssFeedsApi(generics.ListAPIView):
    authentication_classes = (SessionAuthentication, BasicAuthentication)
    permission_classes = (IsAuthenticated,)

    queryset = Organization.active.all().exclude(rss_course_feed='')
    serializer_class = OrganizationRssFeedsApiSerializer


### Login via e-mail key
class LoginKeyCheckView(TemplateView):
    template_name = 'mail-login/login_failed.html'

    def dispatch(self, request, *args, **kwargs):
        key = kwargs.pop('key')
        if LoginKey.objects.filter(key=key).exists():
            today = datetime.datetime.today()
            login_key = LoginKey.objects.get(key=key, pub_date__gte=(today - datetime.timedelta(days=7)))

            login_key.user.backend = 'django.contrib.auth.backends.ModelBackend'
            login(self.request, login_key.user)
            return redirect('/crm/')

        return super(LoginKeyCheckView, self).dispatch(request, *args, **kwargs)


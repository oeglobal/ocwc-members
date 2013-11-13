# -*- coding: utf-8 -*-
import collections

from django.shortcuts import render, redirect
from django.contrib.auth.forms import AuthenticationForm
from django.core.urlresolvers import reverse_lazy, reverse
from django import forms

from vanilla import ListView, DetailView, TemplateView, RedirectView, UpdateView, CreateView
from braces.views import LoginRequiredMixin, StaffuserRequiredMixin

from rest_framework.response import Response
from rest_framework.decorators import api_view, renderer_classes
from rest_framework import generics
from rest_framework.renderers import JSONRenderer, JSONPRenderer, BrowsableAPIRenderer

from .models import Organization, Contact, Address, ReportedStatistic, Country, MembershipApplication
from .serializers import OrganizationApiSerializer, OrganizationDetailedApiSerializer
from .forms import MembershipApplicationModelForm

def index(request):
	if request.user.is_staff:
		return redirect('/staff/')
	elif request.user.is_authenticated():
		return redirect('/crm/')

	ctx = {
		'form': AuthenticationForm,
		'next': '/'
	}
	return render(request, 'index.html', ctx)


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
				  'logo_large', 'logo_small', 'rss_course_feed',]

class OrganizationModelForm(forms.ModelForm):
	class Meta:
		model = Organization
		fields = ['display_name', 'main_website', 'ocw_website', 'description', 
				  'logo_large', 'logo_small', 'rss_course_feed',]

class OrganizationEdit(OrganizationView, UpdateView):
	model = Organization
	template_name = 'organization_edit.html'

	def get_form_class(self):
		if self.request.user.is_staff:
			return OrganizationStaffModelForm
		return OrganizationModelForm

class ReportedStatisticDetailView(OrganizationView, DetailView):
	model = ReportedStatistic
	template_name = 'reported_statistic_view.html'
	context_object_name = 'statistic_list'

	def get_object(self):
		org = Organization.objects.get(pk=self.kwargs['pk'])
		return ReportedStatistic.objects.filter(organization=org).order_by('report_date')

class ReportedStatisticModelForm(forms.ModelForm):
	class Meta:
		model = ReportedStatistic
		fields = ( 'site_visits', 'orig_courses', 'trans_courses', 'orig_course_lang', 
				   'trans_course_lang', 'oer_resources', 'trans_oer_resources', 'comment', 'report_date')

class ReportedStatisticEditView(OrganizationView, UpdateView):
	model = ReportedStatistic
	template_name = 'reported_statistic_edit.html'
	context_object_name = 'stat'
	form_class = ReportedStatisticModelForm

class ReportedStatisticAddView(OrganizationView, CreateView):
	model = ReportedStatistic
	template_name = 'reported_statistic_add.html'
	context_object_name = 'stat'
	form_class = ReportedStatisticModelForm

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
	# 	return MembershipApplication.objects.get(view_link_key=self.kwargs['view_link_key'])

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

# class StaffIndex(StaffView, RedirectView):
# 	permanent = False
# 	url = '/staff/organization/list/'

class OrganizationStaffView(StaffView):
	model = Organization

class OrganizationStaffListView(OrganizationStaffView, ListView):
	template_name = 'staff/organization_list.html'

	def get_queryset(self):
		return self.model.objects.filter(membership_status__in=(2,3,4,5,7,99)).order_by('display_name')

class OrganizationStaffDetailView(OrganizationStaffView, DetailView):
	template_name = 'staff/organization_detail.html'
	context_object_name = 'org'

### API views

@api_view(['GET'])
@renderer_classes([BrowsableAPIRenderer, JSONRenderer, JSONPRenderer])
def address_geo_list_view(request):
	features_list = []

	seen_organizations = []
	for address in Address.objects.filter(latitude__isnull=False, 
										  organization__membership_status__in=(2,3,7)).select_related():

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
	data_list = Address.objects.filter(country__isnull=False, organization__membership_status__in=(2,3,7)) \
			.order_by('country') \
			.values_list('country', flat=True) \
			.distinct()
	data = Country.objects.filter(pk__in=data_list).order_by('name').values_list('name', flat=True)

	return Response(data)

class OrganizationByCountryListViewApi(generics.ListAPIView):
	serializer_class = OrganizationApiSerializer

	def get_queryset(self):
		organization_list = Address.objects.filter(
												country__name=self.kwargs.get('country'),
												organization__membership_status__in=(2,3,5,7)	
											) \
											.values_list('organization', flat=True) \
											.distinct()
		return Organization.objects.filter(pk__in=organization_list).order_by('display_name')

@api_view(['GET'])
def organization_group_by_membership_view(request):
	data = collections.OrderedDict([
		('Institutions of Higher Education', OrganizationApiSerializer(Organization.active.filter(membership_type__in=(5,10,11,12,9,17)), many=True).data),
		('Associate Consortia', OrganizationApiSerializer(Organization.active.filter(membership_type__in=(7,14)), many=True).data),
		('Organizational Members', OrganizationApiSerializer(Organization.active.filter(membership_type__in=(6,13)), many=True).data),
		('Corporate Members', OrganizationApiSerializer(Organization.active.filter(membership_type__in=(8,15,16)), many=True).data),
	])

	return Response(data)

class OrganizationViewApi(generics.RetrieveAPIView):
	queryset = Organization.active.all()
	serializer_class = OrganizationDetailedApiSerializer
# -*- coding: utf-8 -*-
from django.shortcuts import render, redirect

from django.contrib.auth.forms import AuthenticationForm
from django.core.urlresolvers import reverse_lazy, reverse
from django import forms

from vanilla import ListView, DetailView, TemplateView, RedirectView, UpdateView
from braces.views import LoginRequiredMixin, StaffuserRequiredMixin

from rest_framework.response import Response
from rest_framework.decorators import api_view, renderer_classes
from rest_framework import generics
from rest_framework.renderers import JSONRenderer, JSONPRenderer, BrowsableAPIRenderer

from .models import Organization, Contact, Address

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

### Staff specific views

class StaffView(LoginRequiredMixin, StaffuserRequiredMixin):
	pass

# class StaffIndex(StaffView, TemplateView):
# 	template_name = 'staff/index.html'

class StaffIndex(StaffView, RedirectView):
	permanent = False
	url = '/staff/organization/list/'

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
	for address in Address.objects.filter(latitude__isnull=False, organization__membership_status__in=(2,3,7)).select_related():
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
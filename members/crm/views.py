from django.shortcuts import render, redirect

from django.contrib.auth.forms import AuthenticationForm
from django.core.urlresolvers import reverse_lazy, reverse
from django import forms

from django.views.generic import ListView, DetailView, TemplateView, RedirectView, UpdateView
from braces.views import LoginRequiredMixin, StaffuserRequiredMixin

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
	template_name = "organization_view.html"
	context_object_name = "org"

class OrganizationModelForm(forms.ModelForm):
	class Meta:
		model = Organization
		fields = ['display_name', 'main_website', 'ocw_website', 'description', 'logo_large', 'logo_small', 'rss_course_feed',]

class OrganizationEdit(OrganizationView, UpdateView):
	model = Organization
	form_class = OrganizationModelForm
	template_name = 'organization_edit.html'

	def get_object(self):
		return self.request.user.organization_set.latest('id')

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

	def queryset(self):
		return self.model.objects.filter(membership_status__in=(2,3,4,5,7,99)).order_by('display_name')

class OrganizationStaffDetailView(OrganizationStaffView, DetailView):
	template_name = 'staff/organization_detail.html'
	context_object_name = 'org'
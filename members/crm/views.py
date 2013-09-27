from django.shortcuts import render, redirect

from django.contrib.auth.forms import AuthenticationForm

from django.views.generic import ListView, DetailView, TemplateView, RedirectView
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

	# def queryset(self, kwargs):
	# 	return self.model.objects.get(pk=kwargs)
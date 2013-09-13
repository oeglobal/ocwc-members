from django.shortcuts import render, redirect

from django.contrib.auth.forms import AuthenticationForm

from django.views.generic import ListView, DetailView
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


class OrganizationStaffListView(LoginRequiredMixin, StaffuserRequiredMixin, ListView):
	template_name = 'staff/organization_list.html'
	model = Organization

	def queryset(self):
		return self.model.objects.filter(membership_status__in=(2,3,4,5,7)).order_by('display_name')
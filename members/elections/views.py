# -*- coding: utf-8 -*-
import datetime
from django.shortcuts import render, redirect

from vanilla import CreateView, UpdateView, DetailView, ListView, FormView
from .forms import CandidateAddForm, CandidateEditForm
from .models import Candidate, Election

from crm.models import Organization

class CandidateAddView(FormView):
    form_class = CandidateAddForm
    template_name = "elections/candidate_add.html"

    def dispatch(self, request, *args, **kwargs):
        election = Election.objects.latest('id')
        if election.nominate_until < datetime.datetime.now():
            return render(self.request, 'elections/election_closed_nominations.html')

        return super(CandidateAddView, self).dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        org = Organization.objects.get(pk=form.cleaned_data.get('organization'))
        del(form.cleaned_data['organization'])
        del(form.cleaned_data['terms'])

        candidate = Candidate(**form.cleaned_data)
        candidate.election = Election.objects.latest('id')
        candidate.organization = org
        candidate.save()

        candidate.email_board()
        candidate.email_candidate()

        return render(self.request, 'elections/candidate_add_success.html')

class CandidateEditView(UpdateView):
    form_class = CandidateEditForm
    model = Candidate
    template_name = "elections/candidate_edit.html"

    def get_success_url(self):
        return self.object.get_absolute_edit_url()

class CandidateView(DetailView):
    model = Candidate
    template_name = "elections/candidate_view.html"
    context_object_name = 'candidate'

class ElectionListView(ListView):
    model = Election
    template_name = 'elections/candidate_list.html'
    context_object_name = 'election'
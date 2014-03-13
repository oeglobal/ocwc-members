# -*- coding: utf-8 -*-
import datetime
from django.shortcuts import render, redirect
from django.http import Http404

from vanilla import CreateView, UpdateView, DetailView, ListView, FormView
from .forms import CandidateAddForm, CandidateEditForm, VoteForm
from .models import Candidate, Election, PropositionBallot, CandidateBallot

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

class VoteView(DetailView):
    model = Election
    template_name = 'elections/vote_view.html'
    context_object_name = 'election'

class VoteAddFormView(FormView):
    form_class = VoteForm
    template_name = "elections/vote_form.html"

    def dispatch(self, request, *args, **kwargs):
        self.election = Election.objects.get(pk=kwargs.pop('pk'))

        return super(VoteAddFormView, self).dispatch(request, *args, **kwargs)

    def get_form(self, data=None, files=None, **kwargs):
        org = Organization.objects.get(user=self.request.user)
        self.organization = org

        if not org.can_vote():
            raise Http404

        kwargs['election'] = self.election
        return self.get_form_class()(data, files, **kwargs)

    def form_valid(self, form):
        cleaned_data = form.cleaned_data

        proposition_ballot = PropositionBallot.objects.create(
            election = self.election,
            organization = self.organization,
            voter_name = cleaned_data.get('name')
        )

        institutional_ballot = CandidateBallot.objects.create(
            election = self.election,
            organization = self.organization,
            voter_name = cleaned_data.get('name'),
            seat_type = 'institutional'
        )

        for candidate_id in cleaned_data.get('institutional_candidates'):
            candidate = Candidate.objects.get(pk=candidate_id)
            institutional_ballot.votes.add(candidate)

        organizational_ballot = CandidateBallot.objects.create(
            election = self.election,
            organization = self.organization,
            voter_name = cleaned_data.get('name'),
            seat_type = 'organizational'
        )

        for candidate_id in cleaned_data.get('organizational_candidates'):
            candidate = Candidate.objects.get(pk=candidate_id)
            organizational_ballot.votes.add(candidate)

# -*- coding: utf-8 -*-
from django.core.management.base import BaseCommand

from elections.models import Election, PropositionBallot, Candidate

class Command(BaseCommand):
    help = "displays election results in the console"

    def handle(self, *args, **options):
    	election = Election.objects.get(pk=1)
    	self.stdout.write(election.title)

    	self.stdout.write('---')
    	self.stdout.write('Name change ballot')
    	self.stdout.write('Ballots received: %s' % PropositionBallot.objects.filter(election=election).count())
    	self.stdout.write('\tVoted for: %s' % PropositionBallot.objects.filter(election=election, vote=True).count())
    	self.stdout.write('\tVoted against: %s' % PropositionBallot.objects.filter(election=election, vote=False).count())
    	self.stdout.write('\tAbstained: %s' % PropositionBallot.objects.filter(election=election, vote=None).count())

    	self.stdout.write('---')

    	names = []
    	for candidate in Candidate.objects.filter(vetted=True, seat_type='institutional'):
    		 names.append('Votes: %s, %s %s' % (candidate.candidateballot_set.count(), candidate.candidate_first_name, candidate.candidate_last_name))

    	names.sort(reverse=True)
    	self.stdout.write('Institutional board seat')
    	for name in names:
    		self.stdout.write('\t'+name)

    	self.stdout.write('---')
    	names = []
    	for candidate in Candidate.objects.filter(vetted=True, seat_type='organizational'):
    		 names.append('Votes: %s, %s %s' % (candidate.candidateballot_set.count(), candidate.candidate_first_name, candidate.candidate_last_name))

    	names.sort(reverse=True)
    	self.stdout.write('Organizational board seat')
    	for name in names:
    		self.stdout.write('\t'+name)


    	self.stdout.write('---')
    	self.stdout.write('Members that voted:')
    	for ballot in PropositionBallot.objects.filter(election=election).order_by('organization__display_name'):
    		self.stdout.write('%s, %s' % (ballot.organization.display_name, ballot.voter_name))
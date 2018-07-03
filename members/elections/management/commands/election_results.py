# -*- coding: utf-8 -*-
from django.core.management.base import BaseCommand

from elections.models import Election, PropositionBallot, Proposition, Candidate, CandidateBallot


class Command(BaseCommand):
    help = "displays election results in the console"

    def handle(self, *args, **options):
        election = Election.objects.get(pk=6)
        self.stdout.write(election.title)

        for proposition in election.proposition_set.all():
            self.stdout.write('---')
            self.stdout.write(proposition.title)
            self.stdout.write(
                'Ballots received: %s' % PropositionBallot.objects.filter(proposition=proposition).count())
            self.stdout.write(
                '\tVoted for: %s' % PropositionBallot.objects.filter(proposition=proposition, vote=True).count())
            self.stdout.write(
                '\tVoted against: %s' % PropositionBallot.objects.filter(proposition=proposition, vote=False).count())
            self.stdout.write(
                '\tAbstained: %s' % PropositionBallot.objects.filter(proposition=proposition, vote=None).count())
            self.stdout.write('---')

        names = []
        for candidate in Candidate.objects.filter(vetted=True, seat_type='institutional', election=election):
            names.append('Votes: %02d, %s %s' % (
            candidate.candidateballot_set.count(), candidate.candidate_first_name, candidate.candidate_last_name))

        names.sort(reverse=True)
        self.stdout.write('Institutional board seat')
        for name in names:
            self.stdout.write('\t' + name)

        self.stdout.write('---')
        names = []
        for candidate in Candidate.objects.filter(vetted=True, seat_type='organizational', election=election):
            names.append('Votes: %02d, %s %s' % (
            candidate.candidateballot_set.count(), candidate.candidate_first_name, candidate.candidate_last_name))

        names.sort(reverse=True)
        self.stdout.write('Organizational board seat')
        for name in names:
            self.stdout.write('\t' + name)

        self.stdout.write('---')
        self.stdout.write(
            'Members that voted: ({})'.format(CandidateBallot.objects.filter(election=election).count()))
        for ballot in CandidateBallot.objects.filter(election=election).order_by('organization__display_name'):
            self.stdout.write('%s, %s' % (ballot.organization.display_name, ballot.voter_name))

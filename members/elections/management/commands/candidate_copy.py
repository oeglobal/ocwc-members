# -*- coding: utf-8 -*-
from django.core.management.base import BaseCommand
from optparse import make_option

from elections.models import Election, PropositionBallot, Proposition, Candidate


class Command(BaseCommand):
    help = "copies nomination from one election to another"
    option_list = BaseCommand.option_list + (
        make_option("--target-election", action="store", dest="target_election_id", help=""),
        make_option("--candidate", action="store", dest="candidate_id", help=""),
    )

    def handle(self, *args, **options):
        candidate = Candidate.objects.get(pk=options.get('candidate_id'))
        candidate.pk = None
        candidate.election = Election.objects.get(pk=options.get('target_election_id'))
        candidate.save()

        self.stdout.write("Copied {}{} to {}".format(candidate.candidate_first_name, candidate.candidate_last_name,
                                                     candidate.election.title))

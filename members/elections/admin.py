from django.contrib import admin

from .models import Candidate, Election, CandidateBallot, Proposition, PropositionBallot

admin.site.register(Election)
admin.site.register(Candidate)
# admin.site.register(CandidateBallot)
admin.site.register(Proposition)
admin.site.register(PropositionBallot)
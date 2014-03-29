from django.contrib import admin

from .models import Candidate, Election, CandidateBallot, Proposition, PropositionBallot

class PropositionBallotAdmin(admin.ModelAdmin):
	list_display = ('organization',)
	search_fields = ('organization__display_name',)

class CandidateBallotAdmin(admin.ModelAdmin):
	list_display = ('organization', 'seat_type')
	search_fields = ('organization__display_name',)

# admin.site.register(Election)
# admin.site.register(Candidate)
# admin.site.register(CandidateBallot, CandidateBallotAdmin)
# admin.site.register(Proposition)
# admin.site.register(PropositionBallot, PropositionBallotAdmin)
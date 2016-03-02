from django.contrib import admin

from .models import Candidate, Election, CandidateBallot, Proposition, PropositionBallot

class PropositionBallotAdmin(admin.ModelAdmin):
	list_display = ('organization',)
	search_fields = ('organization__display_name',)
	list_filter = ('election',)

class CandidateBallotAdmin(admin.ModelAdmin):
	list_display = ('organization', 'seat_type')
	search_fields = ('organization__display_name',)
	list_filter = ('election',)

class CandidateAdmin(admin.ModelAdmin):
    list_display = ['organization', 'candidate_first_name', 'candidate_last_name', 'status', 'vetted', 'seat_type', ]
    list_filter = ['election', 'vetted', 'status']

admin.site.register(Election)
admin.site.register(Candidate, CandidateAdmin)
# admin.site.register(CandidateBallot, CandidateBallotAdmin)
admin.site.register(Proposition)
# admin.site.register(PropositionBallot, PropositionBallotAdmin)

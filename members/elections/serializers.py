from rest_framework import serializers

from .models import Election, Candidate

class CandidatePublicSerializer(serializers.ModelSerializer):
	organization = serializers.CharField(source='organization.display_name')
	class Meta:
		model = Candidate
		fields = ('candidate_first_name', 'candidate_last_name', 'candidate_job_title', 
				  'biography', 'vision', 'ideas', 'expertise', 'external_url', 'seat_type', 'organization')

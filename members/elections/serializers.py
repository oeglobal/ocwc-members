from rest_framework import serializers

from .models import Election, Candidate


class CandidatePublicSerializer(serializers.ModelSerializer):
    organization = serializers.CharField(source='organization.display_name')
    expertise = serializers.SerializerMethodField()

    class Meta:
        model = Candidate
        fields = ('candidate_first_name', 'candidate_last_name', 'candidate_job_title',
                  'biography', 'vision', 'ideas', 'expertise', 'expertise_other', 'expertise_expanded',
                  'external_url', 'seat_type', 'organization', 'reason')

    def get_expertise(self, obj):
        return ', '.join(obj.get_expertise_items())

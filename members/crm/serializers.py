from rest_framework import serializers

from .models import Organization

class OrganizationApiSerializer(serializers.ModelSerializer):
	membership_type = serializers.CharField(source='get_membership_type_display')
	membership_status = serializers.CharField(source='get_membership_status_display')
	class Meta:
		model = Organization
		fields = ('display_name', 'membership_type', 'membership_status', 'associate_consortium')

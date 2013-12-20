from rest_framework import serializers

from .models import Organization

class OrganizationApiSerializer(serializers.ModelSerializer):
	name = serializers.CharField(source='display_name')
	membership_type = serializers.CharField(source='get_membership_type_display')
	membership_status = serializers.CharField(source='get_membership_status_display')
	class Meta:
		model = Organization
		fields = ('id', 'name', 'membership_type', 'membership_status', 'associate_consortium')

class OrganizationDetailedApiSerializer(OrganizationApiSerializer):
	class Meta:
		model = Organization
		fields = ('id', 'name', 'membership_type', 'membership_status', 'associate_consortium', 
				  'display_name', 'main_website', 'ocw_website', 'description', 'logo_small')

class OrganizationRssFeedsApiSerializer(serializers.ModelSerializer):
	name = serializers.CharField(source='display_name')
	class Meta:
		model = Organization
		fields = ('id', 'name', 'crmid', 'rss_course_feed')

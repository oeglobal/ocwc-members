from rest_framework import serializers

from .models import Organization

US_STATES = {'AL': 'Alabama', 'AK': 'Alaska', 'AZ': 'Arizona', 'AR': 'Arkansas', 'CA': 'California', 'CO': 'Colorado',
             'CT': 'Connecticut', 'DE': 'Delaware', 'FL': 'Florida', 'GA': 'Georgia', 'HI': 'Hawaii', 'ID': 'Idaho',
             'IL': 'Illinois', 'IN': 'Indiana', 'IA': 'Iowa', 'KS': 'Kansas', 'KY': 'Kentucky', 'LA': 'Louisiana',
             'ME': 'Maine', 'MD': 'Maryland', 'MA': 'Massachusetts', 'MI': 'Michigan', 'MN': 'Minnesota',
             'MS': 'Mississippi', 'MO': 'Missouri', 'MT': 'Montana', 'NE': 'Nebraska', 'NV': 'Nevada',
             'NH': 'New Hampshire', 'NJ': 'New Jersey', 'NM': 'New Mexico', 'NY': 'New York', 'NC': 'North Carolina',
             'ND': 'North Dakota', 'OH': 'Ohio', 'OK': 'Oklahoma', 'OR': 'Oregon', 'PA': 'Pennsylvania',
             'RI': 'Rhode Island', 'SC': 'South Carolina', 'SD': 'South Dakota', 'TN': 'Tennessee', 'TX': 'Texas',
             'UT': 'Utah', 'VT': 'Vermont', 'VA': 'Virginia', 'WA': 'Washington', 'WV': 'West Virginia',
             'WI': 'Wisconsin', 'WY': 'Wyoming'}


class OrganizationApiSerializer(serializers.ModelSerializer):
    name = serializers.CharField(source='display_name')
    membership_type = serializers.CharField(source='get_simplified_membership')
    membership_status = serializers.CharField(source='get_membership_status_display')
    state = serializers.SerializerMethodField()

    class Meta:
        model = Organization
        fields = ('id', 'name', 'membership_type', 'membership_status', 'associate_consortium',
                  'logo_large', 'logo_small', 'state', 'main_website')

    def get_state(self, obj):
        if obj.address_set.count():
            state_province = obj.address_set.first().state_province
            if state_province in US_STATES:
                return US_STATES[state_province]

            return state_province


class OrganizationDetailedApiSerializer(OrganizationApiSerializer):
    logo_small_url = serializers.CharField(source='get_logo_small_url')

    class Meta:
        model = Organization
        fields = ('id', 'name', 'membership_type', 'membership_status', 'associate_consortium',
                  'display_name', 'main_website', 'ocw_website', 'description', 'logo_small', 'logo_small_url',
                  'initiative_description1', 'initiative_url1', 'initiative_description2', 'initiative_url2',
                  'initiative_description3', 'initiative_url3', )


class OrganizationRssFeedsApiSerializer(serializers.ModelSerializer):
    name = serializers.CharField(source='display_name')

    class Meta:
        model = Organization
        fields = ('id', 'name', 'crmid', 'rss_course_feed')

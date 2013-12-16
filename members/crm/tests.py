# -*- coding: utf-8 -*-
from django.core.urlresolvers import reverse

from django.test import TransactionTestCase as TestCase
from django.test import Client


class MembershipApplicationTest(TestCase):
    fixtures = ['country.json']

    def setUp(self):
        self.client = Client()

    def testFormSubmission(self):
        from crm.models import MembershipApplication

        data = {'simplified_membership_type': 'institutional',
                'moa_terms': 'on',
                'support_commitment': 'Test support Commitment',
                'display_name': 'Test Institution Name',
                'description': 'Test description',
                'organization_type': 'university',
                'is_accredited': '0',
                'accreditation_body': '',
                'main_website': 'http://example.com',
                'ocw_website': 'http://example.com/ocw/',
                'street_address': 'PO Box 251',
                'supplemental_address_1': '',
                'supplemental_address_2': '',
                'city': 'Newton',
                'postal_code': '02464',
                'state_province': 'MA',
                'country': 227,
                'first_name': 'John',
                'last_name': 'Smith',
                'job_title': 'Director of open studies',
                'email': 'john@example.com',
                'terms_of_use': 'on',
                'coppa': 'on',
                'save': 'save'
            }

        response = self.client.post(reverse('application:application-add'), data)        
        app_id = MembershipApplication.objects.latest('id')

        self.assertRedirects(response, '/application/view/%s/' % app_id.view_link_key )
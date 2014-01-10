# -*- coding: utf-8 -*-
from django.core.urlresolvers import reverse
from django.core import mail

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
        app = MembershipApplication.objects.latest('id')

        self.assertRedirects(response, '/application/view/%s/' % app.view_link_key )

        # check that we send notification email
        self.assertEqual(len(mail.outbox), 1)
        email = mail.outbox.pop()

        self.assertIn('New Membership Application: %s' % app.display_name, email.subject )
        self.assertIn(app.get_absolute_url(), email.body )

class OrganizationApiViewsTest(TestCase):
    fixtures = ['country.json', 'organization.json']

    def setUp(self):
        self.client = Client()

    def testOrganizationRssFeedsApi(self):
        from django.contrib.auth.models import User

        # check that unauthorized requests fail
        response = self.client.get(reverse('api:organization-feeds'))
        self.assertEqual(response.status_code, 403)

        # create user and check that we get feed
        user = User.objects.create_user(username='feed_api_client', email='test@example.com', password='example_pass_123')
        self.client.login(username='feed_api_client', password='example_pass_123')

        response = self.client.get(reverse('api:organization-feeds'))
        self.assertContains(response, 'http://www.ocwconsortium.org/feed/')

        # cleanup
        self.client.logout()
        user.delete()

class TestLoginKey(TestCase):
    fixtures = ['country.json', 'organization.json']

    def setUp(self):
        self.client = Client()

    def testRequestLoginKey(self):
        from crm.models import LoginKey

        response = self.client.post('/', {'email': 'wrong@example.com', 'organization': 1})
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'E-mail you entered is not associated with selected organization')

        response = self.client.post('', {'email': 'tech@ocwconsortium.org', 'organization': 1})
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'E-mail sent')

        login_key = LoginKey.objects.latest('id')
        self.assertEqual(login_key.email, 'tech@ocwconsortium.org')

        self.assertEqual(len(mail.outbox), 1)
        email = mail.outbox.pop()

        self.assertIn('OCW Member portal login information', email.subject )
        self.assertIn(login_key.get_absolute_url(), email.body)
        
        response = self.client.get(login_key.get_absolute_url()+'fail/')
        self.assertNotIn('_auth_user_id', self.client.session)
        self.assertContains(response, 'Login failed')

        response = self.client.get(login_key.get_absolute_url())
        self.assertRedirects(response, '/crm/')
        self.assertIn('_auth_user_id', self.client.session)

        #cleanup
        self.client.logout()        

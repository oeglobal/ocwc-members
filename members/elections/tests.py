from django.core import mail
from django.core.urlresolvers import reverse

from django.test import TransactionTestCase as TestCase
from django.test import Client

class NominationFormTest(TestCase):
    fixtures = ['country.json', 'organization.json', 'election.json']
    
    def setUp(self):
        self.client = Client()

    def testNomination(self):
        data = {
            'terms': 'checked',
            'candidate_first_name': u'John',
            'candidate_last_name': u'Smith',
            'candidate_phone_number': u'01 123 123 123',


            'sponsor_email': u'submitter@example.com',
            'reason': u'Lorem ipsum dolor sit amet, consectetur adipisicing elit, sed do eiusmod\r\ntempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam,\r\nquis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo\r\nconsequat.',
            'sponsor_first_name': u'James',
            'organization': 1,
            'candidate_email': u'nominee@example.com',
            'sponsor_last_name': u'Johnson',
            'candidate_job_title': u'Sample job title'
        }

        response = self.client.post(reverse('elections:candidate-add'), data)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Thank you for submitting your nomination')

        self.assertEqual(len(mail.outbox), 2)
        email = mail.outbox.pop()

        self.assertIn('You have been nominated to serve on the OCWC Board of Directors', email.subject )
        self.assertIn('has nominated you as a candidate for the Board of Directors', email.body)
        #assert edit link

        email = mail.outbox.pop()

        self.assertIn("John Smith was nominated for OCWC board", email.subject)
        self.assertIn("as a candidate for the board of directors", email.body)
        #assert view link

# -*- coding: utf-8 -*-
from django.core import mail
from django.core.urlresolvers import reverse

from django.test import TransactionTestCase as TestCase
from django.test import Client

class NominationFormTest(TestCase):
    fixtures = ['country.json', 'organization.json', 'election.json']
    
    def setUp(self):
        self.client = Client()

    def testNomination(self):
        from .models import Candidate

        data = {
            'terms': 'checked',
            'candidate_first_name': u'Đohn',
            'candidate_last_name': u'Šmith',
            'candidate_phone_number': u'01 123 123 123',


            'sponsor_email': u'submitter@example.com',
            'reason': u'Lorem ipsum dolor sit amet, consectetur adipisicing elit, sed do eiusmod\r\ntempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam,\r\nquis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo\r\nconsequat.',
            'sponsor_first_name': u'Jameš',
            'organization': 1,
            'candidate_email': u'nominee@example.com',
            'sponsor_last_name': u'Johnčon',
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

        self.assertIn(u"Đohn Šmith was nominated for OCWC board", email.subject)
        self.assertIn("as a candidate for the board of directors", email.body)
        #assert view link

        Candidate.objects.last().delete()

    def testVotingProcedure(self):
        from crm.models import Organization, LoginKey
        from elections.models import Candidate, Election, Proposition

        election = Election.objects.get(pk=1)

        candidate_data = {
                'candidate_first_name': u'Đohn',
                'candidate_last_name': u'Šmith',
                'candidate_phone_number': u'01 123 123 123',
                'sponsor_email': u'submitter@example.com',
                'reason': u'Lorem ipsum dolor sit amet, ',
                'sponsor_first_name': u'Jameš',
                'organization': Organization.objects.get(pk=1),
                'candidate_email': u'nominee@example.com',
                'sponsor_last_name': u'Johnčon',
                'candidate_job_title': u'Sample job title',
                'election': election,
                'vetted': True,
                'seat_type': 'institutional'
        }

        candidate_john = Candidate.objects.create(**candidate_data)


        candidate_data.update({
            'candidate_first_name': u'Mike',
            'organization': Organization.objects.get(pk=1),
        })

        candidate_mike = Candidate.objects.create(**candidate_data)

        candidate_data.update({
            'candidate_first_name': u'Mary',
            'organization': Organization.objects.get(pk=2),
        })
        candidate_mary = Candidate.objects.create(**candidate_data)

        candidate_data.update({
            'candidate_first_name': u'James',
            'organization': Organization.objects.get(pk=3),
            'vetted': False
        })
        candidate_james = Candidate.objects.create(**candidate_data)


        proposition = Proposition.objects.create(
            election = election,
            title = 'Proposition Title',
            description = 'Example proposition content'
        )

        # log us in
        self.client.post('', {'email': 'tech@ocwconsortium.org', 'organization': 1})
        login_key = LoginKey.objects.latest('id')
        mail.outbox.pop()
        self.client.get(login_key.get_absolute_url())

        response = self.client.get('/elections/vote/add/1/')
        self.assertEqual(response.status_code, 200)

        # print response.content

        self.assertContains(response, proposition.title)
        self.assertContains(response, proposition.description)

        self.assertContains(response, u'Đohn Šmith')
        self.assertContains(response, u'Mike Šmith')
        self.assertContains(response, u'Mary Šmith')
        
        self.assertNotContains(response, u'James')
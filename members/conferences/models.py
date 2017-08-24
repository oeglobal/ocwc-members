# -*- coding: utf-8 -*-
import os
import uuid
import subprocess

from django.db import models
from django.core.urlresolvers import reverse
from django.core.mail import EmailMessage
from django.conf import settings

here = lambda x: os.path.join(os.path.dirname(os.path.abspath(__file__)), x)

class ConferenceInterface(models.Model):
    name = models.CharField(max_length=255)
    url = models.CharField(max_length=255, default='')
    api_key = models.CharField(max_length=255, default='')
    private_key = models.CharField(max_length=255, default='')

    last_synced = models.DateTimeField(null=True)

    def __unicode__(self):
        return self.name

class ConferenceRegistration(models.Model):
    PAYMENT_TYPE = (
        ('paypal', 'PayPal'),
        ('wire', 'Wire Transfer')
    )

    interface = models.ForeignKey(ConferenceInterface)
    form_id = models.CharField(max_length=255)
    entry_id = models.CharField(max_length=255)
    entry_created = models.DateTimeField(null=True)

    name = models.CharField(max_length=255, default='')
    email = models.CharField(max_length=255, default='')
    organization = models.CharField(max_length=255, default='')
    billing_address = models.TextField(default='')

    ticket_type = models.CharField(max_length=255)
    dinner_guest = models.CharField(max_length=255, default='')
    conference_dinner = models.CharField(max_length=255, default='')
    reception_guest = models.CharField(max_length=255, default='')
    total_amount = models.CharField(max_length=255)
    payment_type = models.CharField(choices=PAYMENT_TYPE, max_length=255)

    source_url = models.CharField(max_length=255)

    last_synced = models.DateTimeField(auto_now=True)
    access_key = models.CharField(max_length=32, blank=True)

    def save(self, force_insert=False, force_update=False, using=None):
        if not self.access_key:
            self.access_key = uuid.uuid4().get_hex()

        super(ConferenceRegistration, self).save(force_insert=force_insert, force_update=force_update, using=using)

    def get_access_key_url(self):
        return reverse('conferences:invoice_preview', kwargs={'pk': self.id, 'access_key':self.access_key})

    def email_invoice(self):
        body = """Thank you for registering for the Open Education Global Conference 2017 (8-10 March in Cape Town, South Africa).

Attached is your invoice.

Do not hesitate to contact us at conference@oeconsortium.org if you have any questions.
We look forward to welcoming you in South Africa.

Open Education Global Conference 2017 Planning Team.
"""

        message = EmailMessage(
            subject = 'Open Education Global Conference 2018 - Invoice',
            body = body,
            from_email = 'conference@oeconsortium.org',
            to = [self.email],
            # bcc = ['conference@oeconsortium.org']
        )


        url = '%s%s' % (settings.INVOICES_PHANTOM_JS_HOST, self.get_access_key_url())

        pdf = '/tmp/oeglobal_invoice_{}.pdf'.format(uuid.uuid4().get_hex())
        popen_instance = subprocess.Popen([here('../../bin/phantomjs'),
                          here('../crm/phantomjs-scripts/rasterize.js'),
                          url,
                          pdf,
                          'Letter'
                        ])

        subprocess.Popen.wait(popen_instance)

        with open(pdf, 'r') as pdf_file:
            message.attach(filename='OEGlobal-Invoice-%s.pdf' % self.entry_id,
                           content=pdf_file.read(),
                           mimetype='application/pdf')
            message.send()

import uuid

from django.db import models
from django.core.urlresolvers import reverse

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

    ticket_type = models.CharField(max_length=255)
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

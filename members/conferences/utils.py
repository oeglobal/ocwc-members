# -*- coding: utf-8 -*-
import arrow
import hmac
import hashlib
import requests
import json

from pprint import pprint

from .models import ConferenceInterface, ConferenceRegistration

def _calculate_signature( string, private_key):
    hash_var = hmac.new(str(private_key), string, hashlib.sha1).digest()
    sig = hash_var.encode('base64')

    return sig

def sync_conference(conf_id=1):
    conf = ConferenceInterface.objects.get(pk=conf_id)

    route = "forms/1/entries"
    expires = arrow.utcnow().replace(minutes=+10).timestamp

    string_to_sign = str("{}:{}:{}:{}".format(conf.api_key, 'GET', route, expires))
    sig = _calculate_signature(string_to_sign, conf.private_key)
    req = requests.get(conf.url, params={'api_key': conf.api_key,
                                       'signature': sig,
                                       'expires': expires})

    data = json.loads(req.content)

    for entry in data.get('response', {}).get('entries', []):
        if 'wire' in entry.get('21'):
            payment_type = 'wire'
        else:
            payment_type = 'paypal'

        registration, is_created = ConferenceRegistration.objects.get_or_create(
                                        interface=conf,
                                        form_id=1,
                                        entry_id=entry.get('id'),
                                        defaults = {
                                            'ticket_type': entry.get('9'),
                                            'total_amount': entry.get('12'),
                                            'payment_type': payment_type,
                                            'source_url': entry.get('source_url'),
                                            'entry_created': arrow.get(entry.get('date_created').replace(' ', 'T')).datetime,

                                            'name': u"{} {}".format(entry.get('1.3'), entry.get('1.6')),
                                            'email': entry.get('2'),
                                            'organization': entry.get('6'),
                                            'billing_address': entry.get('34'),
                                            'conference_dinner': entry.get('38'),
                                            'reception_guest': entry.get('40'),
                                            'dinner_guest': entry.get('39'),
                                        },
                                    )

        if is_created and registration.payment_type == 'wire':
            registration.email_invoice()


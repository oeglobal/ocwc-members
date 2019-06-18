# -*- coding: utf-8 -*-
import arrow
import hmac
import hashlib
import requests
import json
from pyquery import PyQuery as pq
from bs4 import BeautifulSoup
from html_table_extractor.extractor import Extractor

from django.conf import settings

from .models import ConferenceInterface, ConferenceRegistration


def _calculate_signature(string, private_key):
    hash_var = hmac.new(str(private_key), string, hashlib.sha1).digest()
    sig = hash_var.encode("base64")

    return sig


def sync_conference(conf_id=3):
    conf = ConferenceInterface.objects.get(pk=conf_id)

    route = "forms/1/entries"
    expires = arrow.utcnow().replace(minutes=+10).timestamp

    string_to_sign = str("{}:{}:{}:{}".format(conf.api_key, "GET", route, expires))
    sig = _calculate_signature(string_to_sign, conf.private_key)
    req = requests.get(
        conf.url, params={"api_key": conf.api_key, "signature": sig, "expires": expires}
    )

    data = json.loads(req.content)

    for entry in data.get("response", {}).get("entries", []):
        if entry["status"] == "trash":
            continue

        html = requests.get(
            "{}/wp-json/conference/v1/entry/{}/{}".format(
                settings.WP_URL, entry.get("form_id"), entry.get("id")
            ),
            auth=(settings.WP_BASIC_AUTH_USER, settings.WP_BASIC_AUTH_PASS),
        )

        html = html.json().get("html")

        table = BeautifulSoup(html, "html.parser").find_all(
            "table", class_="entry-products"
        )
        extractor = Extractor(table[0], transformer=unicode)
        extractor.parse()
        table_data = extractor.return_list()

        products = []
        total_amount = ""
        for item in table_data:
            product_name, amount, price, total = item

            if price == "Total":
                total_amount = total
                continue

            product_name = product_name.strip()
            amount = int(amount)
            price = float(price.replace(u"$", "").strip().replace(",", "."))

            products.append({"name": product_name, "amount": amount, "price": price})

        doc = pq(html)
        billing_html = ""
        for val in doc(".entry-view-field-name"):
            if val.text == "Billing address details":
                doc(val).parents("tr").next_all().find("a").remove()
                billing_html = doc(val).parents("tr").next_all().find("td").html()
                if entry.get("34"):
                    billing_html += "<br/>" + entry.get("34")

        billing_html = (
            billing_html.replace("<br/>", "\n").replace("<p>", "").replace("</p>", "")
        )

        if "wire" in entry.get("21"):
            payment_type = "wire"
        else:
            payment_type = "group"

        if entry.get("53"):
            is_group = True
        else:
            is_group = False

        registration, is_created = ConferenceRegistration.objects.get_or_create(
            interface=conf,
            form_id=entry.get("form_id"),
            entry_id=entry.get("id"),
            defaults={
                "ticket_type": entry.get("9"),
                "payment_type": payment_type,
                "source_url": entry.get("source_url"),
                "entry_created": arrow.get(
                    entry.get("date_created").replace(" ", "T")
                ).datetime,
                "name": u"{} {}".format(entry.get("1.3"), entry.get("1.6")),
                "email": entry.get("2"),
                "organization": entry.get("6"),
                "billing_html": billing_html,
                "total_amount": total_amount,
                "products": products,
                "is_group": is_group,
            },
        )

        # if is_created and registration.payment_type == 'wire':
        #     registration.email_invoice()

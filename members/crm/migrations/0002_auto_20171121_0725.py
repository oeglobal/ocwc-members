# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('crm', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='membershipapplication',
            name='membership_type',
            field=models.IntegerField(default=None, null=True, blank=True, choices=[(5, b'Institutional Members'), (10, b'Institutional Members - MRC'), (11, b'Institutional Members - DC'), (12, b'Institutional Members - DC - MRC'), (9, b'Associate Institutional Members'), (17, b'Associate Institutional Members - DC'), (6, b'Organizational Members'), (13, b'Organizational Members - DC'), (18, b'Organizational Members - MRC'), (7, b'Associate Consortium Members'), (14, b'Associate Consortium Members - DC'), (8, b'Corporate Members - Basic'), (15, b'Corporate Members - Premium'), (16, b'Corporate Members - Sustaining')]),
        ),
        migrations.AlterField(
            model_name='organization',
            name='membership_status',
            field=models.IntegerField(choices=[(1, b'Applied'), (2, b'Current'), (3, b'Grace'), (4, b'Expired'), (5, b'Pending'), (6, b'Cancelled'), (7, b'Sustaining'), (99, b'Example')]),
        ),
        migrations.AlterField(
            model_name='organization',
            name='membership_type',
            field=models.IntegerField(choices=[(5, b'Institutional Members'), (10, b'Institutional Members - MRC'), (11, b'Institutional Members - DC'), (12, b'Institutional Members - DC - MRC'), (9, b'Associate Institutional Members'), (17, b'Associate Institutional Members - DC'), (6, b'Organizational Members'), (13, b'Organizational Members - DC'), (18, b'Organizational Members - MRC'), (7, b'Associate Consortium Members'), (14, b'Associate Consortium Members - DC'), (8, b'Corporate Members - Basic'), (15, b'Corporate Members - Premium'), (16, b'Corporate Members - Sustaining')]),
        ),
        migrations.AlterField(
            model_name='organization',
            name='slug',
            field=models.CharField(default=b'', unique=True, max_length=60),
        ),
    ]

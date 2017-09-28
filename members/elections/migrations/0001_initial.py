# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('crm', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Candidate',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('status', models.CharField(default=b'', max_length=60, choices=[(b'nominated', b'Nominated'), (b'accepted', b'Accepted'), (b'declined', b'Declined'), (b'rejected', b'Rejected'), (b'spam', b'Spam')])),
                ('candidate_first_name', models.CharField(max_length=255)),
                ('candidate_last_name', models.CharField(max_length=255)),
                ('candidate_job_title', models.CharField(default=b'', max_length=255, blank=True)),
                ('candidate_email', models.EmailField(max_length=255)),
                ('candidate_phone_number', models.CharField(default=b'', max_length=255, blank=True)),
                ('reason', models.TextField(blank=True)),
                ('sponsor_first_name', models.CharField(max_length=255)),
                ('sponsor_last_name', models.CharField(max_length=255)),
                ('sponsor_email', models.CharField(max_length=255)),
                ('edit_link_key', models.CharField(max_length=255, blank=True)),
                ('view_link_key', models.CharField(max_length=255, blank=True)),
                ('email_alternate', models.CharField(default=b'', max_length=255, blank=True)),
                ('biography', models.TextField(blank=True)),
                ('vision', models.TextField(blank=True)),
                ('ideas', models.TextField(blank=True)),
                ('expertise', models.TextField(blank=True)),
                ('external_url', models.CharField(default=b'', max_length=255, blank=True)),
                ('vetted', models.BooleanField(default=False)),
                ('seat_type', models.CharField(blank=True, max_length=60, choices=[(b'institutional', b'Institutional'), (b'organizational', b'Organizational')])),
                ('pub_date', models.DateTimeField(auto_now_add=True)),
                ('last_modified', models.DateTimeField(auto_now=True)),
                ('order', models.IntegerField(default=0)),
            ],
        ),
        migrations.CreateModel(
            name='CandidateBallot',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('voter_name', models.CharField(max_length=255)),
                ('seat_type', models.CharField(max_length=60, choices=[(b'institutional', b'Institutional'), (b'organizational', b'Organizational')])),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('modified', models.DateTimeField(auto_now=True)),
            ],
        ),
        migrations.CreateModel(
            name='Election',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('title', models.CharField(max_length=255)),
                ('view_nominations_key', models.CharField(max_length=255, blank=True)),
                ('edit_nominations_key', models.CharField(max_length=255, blank=True)),
                ('nominate_until', models.DateTimeField(null=True)),
                ('vote_from', models.DateTimeField(null=True)),
                ('vote_until', models.DateTimeField(null=True)),
            ],
            options={
                'get_latest_by': 'pk',
            },
        ),
        migrations.CreateModel(
            name='Proposition',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('title', models.CharField(max_length=255)),
                ('description', models.TextField(blank=True)),
                ('published', models.BooleanField(default=False)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('modified', models.DateTimeField(auto_now=True)),
                ('election', models.ForeignKey(to='elections.Election')),
            ],
        ),
        migrations.CreateModel(
            name='PropositionBallot',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('voter_name', models.CharField(max_length=255)),
                ('vote', models.NullBooleanField(choices=[(True, b'We vote <strong>for</strong> this proposition'), (False, b'We vote <strong>against</strong> this proposition'), (None, b'We abstain')])),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('modified', models.DateTimeField(auto_now=True)),
                ('election', models.ForeignKey(to='elections.Election')),
                ('organization', models.ForeignKey(to='crm.Organization')),
                ('proposition', models.ForeignKey(to='elections.Proposition')),
            ],
        ),
        migrations.AddField(
            model_name='candidateballot',
            name='election',
            field=models.ForeignKey(to='elections.Election'),
        ),
        migrations.AddField(
            model_name='candidateballot',
            name='organization',
            field=models.ForeignKey(to='crm.Organization'),
        ),
        migrations.AddField(
            model_name='candidateballot',
            name='votes',
            field=models.ManyToManyField(to='elections.Candidate'),
        ),
        migrations.AddField(
            model_name='candidate',
            name='election',
            field=models.ForeignKey(to='elections.Election'),
        ),
        migrations.AddField(
            model_name='candidate',
            name='organization',
            field=models.ForeignKey(to='crm.Organization'),
        ),
    ]

# -*- coding: utf-8 -*-
from __future__ import print_function
from django.core.management.base import BaseCommand, CommandError

from conferences.utils import sync_conference


class Command(BaseCommand):
    help = "synces conference information"

    def add_arguments(self, parser):
        parser.add_argument('id', nargs=1, type=int, help="Conference Interface ID")

    def handle(self, *args, **options):
        if options.get('id'):
            sync_conference(options.get('id')[0])

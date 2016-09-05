# -*- coding: utf-8 -*-
from __future__ import print_function
from django.core.management.base import BaseCommand
from optparse import make_option

from conferences.utils import sync_conference

class Command(BaseCommand):
    help = "synces conference information"

    args = '--id'

    option_list = BaseCommand.option_list + (
        make_option("--id", action="store", dest="id", help="Conference Interface ID"),
    )

    def handle(self, *args, **options):
        if options.get('id'):
            sync_conference(options.get('id'))

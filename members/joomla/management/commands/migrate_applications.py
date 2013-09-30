# -*- coding: utf-8 -*-
from django.core.management.base import BaseCommand

from joomla.models import CivicrmValue1InstitutionInformation, CivicrmMembership, JosMemberApplications, CivicrmContact, JosMemberAppComments
from crm.models import Organization, MembershipApplication, MembershipApplicationComment, Country

CiviInst = CivicrmValue1InstitutionInformation

class Command(BaseCommand):
    help = "migrates membership applications to the new system"
    def handle(self, *args, **options):
        self.stdout.write('Migrating Membership Applications')

        # for civi_membership in CivicrmMembership.objects.all():
        for jos_member in JosMemberApplications.objects.all():
            if jos_member.app_status == 'Spam':
                continue

            # print jos_member.app_id
            try:
                crmid = jos_member.crm_contact_id_org.id
            except CivicrmContact.DoesNotExist:
                print "Application %s: contact %s does not exist, skipping application" % (jos_member.app_id, jos_member.crm_contact_id_org_id)
                continue

            try:
                civi_membership = CivicrmMembership.objects.filter(contact=crmid)[0]
                org = Organization.objects.filter(crmid=crmid)[0]
            except IndexError:
                org = None

            try:
                instinfo = CivicrmValue1InstitutionInformation.objects.get(entity_id=crmid)
            except CivicrmValue1InstitutionInformation.DoesNotExist:
                print "Skipping %s - because CivicrmValue1InstitutionInformation does not exist" % (jos_member.app_id)
                continue

            if instinfo.institution_country:
                country = Country.objects.get(name=instinfo.institution_country.name)
            else:
                country = None

            membership_application = MembershipApplication.objects.create(
                    organization = org,
                    membership_type = civi_membership.membership_type_id,

                    legacy_application_id = jos_member.app_id,
                    legacy_entity_id = crmid,
                    
                    main_website = instinfo.main_website,
                    description = instinfo.description,
                    ocw_website = instinfo.ocw_website,

                    logo_large = instinfo.seal_image__large,
                    logo_small = instinfo.seal_image__small,
                    institution_country = country,

                    rss_course_feed = instinfo.rss_course_feed or '',
                    rss_referral_link = instinfo.rss_referral_link or '',
                    rss_course_feed_language = instinfo.rss_course_feed_language or '',

                    agreed_to_terms = instinfo.agreed_to_terms or '',
                    agreed_criteria = instinfo.agreed_criteria or '',
                    contract_version = instinfo.contract_version or '',

                    ocw_software_platform = instinfo.ocw_software_platform or '',
                    ocw_platform_details = instinfo.ocw_platform_details or '',
                    ocw_site_hosting = instinfo.ocw_site_hosting or '',
                    ocw_site_approved = instinfo.ocw_site_approved or '',
                    ocw_published_languages = instinfo.ocw_published_languages or '',
                    ocw_license = instinfo.ocw_license or '',

                    organization_type = instinfo.organization_type or '',
                    accreditation_body = instinfo.accreditation_body_53 or '',
                    ocw_launch_date = instinfo.ocw_launch_date,
                    support_commitment = instinfo.support_commitment_54 or '',

                    app_status = jos_member.app_status,
                    created = jos_member.cdate,
                    modified = jos_member.mdate
                )

        for jos_app_comment in JosMemberAppComments.objects.filter(app_id=jos_member.app_id):
            comment = MembershipApplicationComment.objects.create(
                application = membership_application,

                legacy_comment_id = jos_app_comment.comment_id,
                legacy_app_id = jos_app_comment.app_id,

                comment = jos_app_comment.comment,
                sent_email = jos_app_comment.sent_email,

                created = jos_app_comment.cdate
            )

        self.stdout.write('Membership Applications Complete')
#!/usr/bin/env python3

import time
import toolbag



class Skim_conf:
    '''
    Configuration Items
    '''
    def show_banner(self):
        '''
        Print the banner
        '''
        tb = toolbag.Toolbag()
        color = "green"
        print(tb.color("\n\n   ▄████████    ▄█   ▄█▄  ▄█    ▄▄▄▄███▄▄▄▄   ", color))
        print(tb.color("  ███    ███   ███ ▄███▀ ███  ▄██▀▀▀███▀▀▀██▄ ", color))
        print(tb.color("  ███    █▀    ███▐██▀   ███▌ ███   ███   ███ ", color))
        print(tb.color("  ███         ▄█████▀    ███▌ ███   ███   ███ ", color))
        print(tb.color("▀███████████ ▀▀█████▄    ███▌ ███   ███   ███ ", color))
        print(tb.color("         ███   ███▐██▄   ███  ███   ███   ███ ", color))
        print(tb.color("   ▄█    ███   ███ ▀███▄ ███  ███   ███   ███ ", color))
        print(tb.color(" ▄████████▀    ███   ▀█▀ █▀    ▀█   ███   █▀ ", color))
        from skim_controller import SkimController as ctrl
        num_domains: int = ctrl().num_domains
        print("\n\nTotal number of domains to be traversed: " + str(num_domains) + "\n")
        print("\n\nOnly domains which are not responding 200OK are printed.\n")
        time.sleep(1.5)



    def whitelist_domains(self):
        '''
        Whitelist "List" data type containing domains which are not used or not applicable to track content.
        '''
        whitelist_domains = [
                          "zone2",
                          "mpe",
                          "res.eq.edu.au",
                          "mail",
                          "smtp",
                          "bullyingnoway.info",
                          "bullyingnoway.net.au",
                          "bullyingnoway.org",
                          "bullyingnoway.org.au",
                          "bundabergsecondaryguidance.eq.edu.au",
                          "cis.eq.edu.au",
                          "citecvsattestschool.eq.edu.au",
                          "corporate-vpn-dr.eq.edu.au",
                          "codingcounts.org.au",
                          "curriculum.qld.gov.au",
                          "codingcounts.biz",
                          "codingcounts.net.au",
                          "skills.qld.gov.au",
                          "wphe.dete.qld.gov.au",
                          "newprimaryschoolinredbankplains.eq.edu.au",
                          "newspecialschoolincairns.eq.edu.au",
                          "newprimaryschoolinredbankplains.eq.edu.au",
                          "advancingeducation.biz",
                          "det.net.au",
                          "deta.com.au",
                          "deta.net.au",
                          "educationqld.com",
                          "mis-ccc.eq.edu.au",
                          "jobsqld.org",
                          "codingcounts.info",
                          "jobsqld.net.au",
                          "educationqld.info",
                          "educationqld.net",
                          "educationqld.net.au",
                          "jobsqueensland.org",
                          "educationqld.org",
                          "educationqueensland.com.au",
                          "educationqueensland.info",
                          "jobsqueensland.net",
                          "educationqueensland.net",
                          "educationqueensland.net.au",
                          "naplanonline.biz",
                          "educationqueensland.org",
                          "eqqld.com",
                          "eqqld.com.au",
                          "eqqld.info",
                          "eqqld.net",
                          "eqqld.net.au",
                          "eqqld.org",
                          "eqqueensland.com",
                          "eqqueensland.com.au",
                          "eqqueensland.info",
                          "eqqueensland.net",
                          "eqqueensland.net.au",
                          "eqqueensland.org",
                          "skillsqueensland.info",
                          "trainingqueensland.net",
                          "trainingqld.info",
                          "trainingqld.net",
                          "oneschool.com.au",
                          "supportingwomen.qld.gov.au",
                          "youthcareersinfo.qld.gov.au",
                          "trainingqld.net.au",
                          "trainingqld.org",
                          "smartclassrooms.org",
                          "skillsqueensland.org",
                          "oecec.com.au",
                          "oneportal.net.au",
                          "skillingsolutions.org",
                          "ministerialindustryCommission.com",
                          "trainingqueensland.net.au",
                          "vetlearningpathways.qld.gov.au",
                          "smartclassrooms.net",
                          "skillingsolutions.qld.gov.au",
                          "trainingqueensland.org",
                          "trainingqueensland.info",
                          "skillsqld.net",
                          "skillsqld.info",
                          "skillsqueensland.net",
                          "educationqld.com",
                          "skillingsolutions.info",
                          "smartclassrooms.com.au",
                          "smartclassrooms.info",
                          "oecec.net",
                          "oecec.org",
                          "skillingsolutions.net",
                          "smartclassrooms.net.au",
                          "skillingsolutions.net.au",
                          "oecec.net.au",
                          "learningplace.net.au",
                          "skillsqld.org",
                          "oneportal.com.au",
                          "qparents.com",
                          "openapi.csb.sit.education.qld.gov.au",
                          "openapi.csb.education.qld.gov.au",
                          "webservice.eq.edu.au",
                          "api.csb.sit.education.qld.gov.au",
                          "api.csb.education.qld.gov.au",
                          "eraauthsvc.dete.qld.gov.au"
                          "oecec.info",
                          "skillsqld.com.au",
                          "portals.byo.eq.edu.au",
                          "oneschool.info",
                          "ns.eq.edu.au",
                          "ns1.eq.edu.au",
                          "ns2.eq.edu.au",
                          "mx.eq.edu.au",
                          "mxa.eq.edu.au",
                          "mxb.eq.edu.au",
                          "domainnameadmin.dete.qld.gov.au ",
                          "discussions.eq.edu.au"
                          ]
        return whitelist_domains


#!/usr/bin/env python3


class Skim_conf:
    '''
    Configuration Items
    '''
    def show_banner(self):
        import toolbag
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

        print(tb.color("\n\nOnly domains which are not responding 200OK are printed.\n", color))


    def whitelist_domains(self):
        '''
        Whitelist "List" data type containing domains which are not used or not applicable to track content.
        '''
        whitelist_domains = [
                        "advancingeducation.biz",
                        "api.csb.education.qld.gov.au",
                        "api.csb.sit.education.qld.gov.au",
                        "bullyingnoway.info",
                        "bullyingnoway.net.au",
                        "bullyingnoway.org",
                        "bullyingnoway.org.au",
                        "bundabergsecondaryguidance.eq.edu.au",
                        "cis.eq.edu.au",
                        "citecvsattestschool.eq.edu.au",
                        "codingcounts.biz",
                        "codingcounts.info",
                        "codingcounts.net.au",
                        "codingcounts.org.au",
                        "corporate-vpn-dr.eq.edu.au",
                        "crazydomains.com.au",
                        "intranet.sit.education.qld.gov.au",
                        "curriculum.qld.gov.au",
                        "DC.date.modified",
                        "det.net.au",
                        "deta.com.au",
                        "deta.net.au",
                        "discussions.eq.edu.au",
                        "domainnameadmin.dete.qld.gov.au ",
                        "educationqld.com",
                        "educationqld.com",
                        "educationqld.info",
                        "educationqld.net",
                        "educationqld.net.au",
                        "educationqld.org",
                        "educationqueensland.com.au",
                        "educationqueensland.info",
                        "educationqueensland.net",
                        "educationqueensland.net.au",
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
                        "eraauthsvc.dete.qld.gov.auoecec.info",
                        "_gaq.push([",
                        "jobsqld.net.au",
                        "jobsqld.org",
                        "jobsqueensland.net",
                        "jobsqueensland.org",
                        "learningplace.net.au",
                        "mail",
                        "ministerialindustryCommission.com",
                        "mis-ccc.eq.edu.au",
                        "mpe",
                        "mx.eq.edu.au",
                        "mxa.eq.edu.au",
                        "mxb.eq.edu.au",
                        "naplanonline.biz",
                        "newprimaryschoolinredbankplains.eq.edu.au",
                        "newprimaryschoolinredbankplains.eq.edu.au",
                        "newspecialschoolincairns.eq.edu.au",
                        "ns.eq.edu.au",
                        "ns1.eq.edu.au",
                        "ns2.eq.edu.au",
                        "oecec.com.au",
                        "oecec.net",
                        "oecec.net.au",
                        "oecec.org",
                        "oneportal.com.au",
                        "oneportal.net.au",
                        "oneschool.com.au",
                        "oneschool.info",
                        "openapi.csb.education.qld.gov.au",
                        "openapi.csb.sit.education.qld.gov.au",
                        "portals.byo.eq.edu.au",
                        "qparents.com",
                        "qparents.net.au",
                        "qschools.org",
                        "reacharts.com.au",
                        "res.eq.edu.au",
                        "skillingsolutions.info",
                        "skillingsolutions.net",
                        "skillingsolutions.net.au",
                        "skillingsolutions.org",
                        "skillingsolutions.qld.gov.au",
                        "skills.qld.gov.au",
                        "skillsqld.com.au",
                        "skillsqld.info",
                        "skillsqld.net",
                        "skillsqld.org",
                        "skillsqueensland.info",
                        "skillsqueensland.net",
                        "skillsqueensland.org",
                        "smartclassrooms.com.au",
                        "smartclassrooms.info",
                        "smartclassrooms.net",
                        "smartclassrooms.net.au",
                        "smartclassrooms.org",
                        "smtp",
                        "supportingwomen.qld.gov.au",
                        "trainingqld.info",
                        "trainingqld.net",
                        "trainingqld.net.au",
                        "trainingqld.org",
                        "trainingqueensland.info",
                        "trainingqueensland.net",
                        "trainingqueensland.net.au",
                        "trainingqueensland.org",
                        "vetlearningpathways.qld.gov.au",
                        "webservice.eq.edu.au",
                        "wphe.dete.qld.gov.au",
                        "youthcareersinfo.qld.gov.au",
                        "zone2"
                                ]
        return whitelist_domains


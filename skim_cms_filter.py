#!/usr/bin/env python3

import skim_writer_io
from time import perf_counter as pc


class SkimCmsFilter:

    def __init__(self):
        self.perf_is_it_drupal = pc
        self.perf_is_it_wordpress = pc
        self.perf_is_it_sharepoint = pc
        self.perf_is_it_joomla = pc

    def is_it_drupal(self, url, headers: str, content: str) -> bool:
        '''
        Parse http response data for Drupal CMS
        '''
        try:
            p1 = pc()
            writer = skim_writer_io.Skim_writer_io().writer
            check = str(headers) + str(content)
            if ("drupal" in check) or ("Drupal" in check):
                writer(url, "drupal")
                p2 = pc()
                self.perf_is_it_drupal = p2 - p1
                return True
        except Exception as e:
            print("Error! in drupal: " + str(e))

    def is_it_wordpress(self, url: str, headers: str) -> bool:
        '''
        Parse http response data for Wordpress CMS
        '''
        try:
            p1 = pc()
            writer = skim_writer_io.Skim_writer_io().writer
            headers = str(headers)
            if ("wp" in headers) or ("xmlrpc.php" in headers):
                writer(url, "wordpress")
                p2 = pc()
                self.perf_is_it_wordpress = p2 - p1
                return True
        except Exception as e:
            print("Error! in is_it_wordpress " + str(e))

    def is_it_sharepoint(self, url: str, headers: str) -> bool:
        '''
        Parse http response data for Sharepoint
        '''
        try:
            p1 = pc()
            writer = skim_writer_io.Skim_writer_io().writer
            if (("MicrosoftSharePointTeamServices" in headers)
            or ("access-keys-sharepoint-schools.html" in headers)):
                writer(url, "sharepoint")
                p2 = pc()
                self.perf_is_it_sharepoint = p2 - p1
                return True
        except Exception as e:
            print("Error! in is_it_sharepoint: " + str(e))

    def is_it_joomla(self, url: str, headers: str, content: str) -> bool:
        '''
        Parse http response data for Joomla CMS
        '''
        try:
            p1 = pc()
            writer = skim_writer_io.Skim_writer_io().writer
            search_space = str(headers) + str(content)
            if "joomla" in search_space:
                writer(url, "joomla")
                p2 = pc()
                self.perf_is_it_joomla = p2 - p1
                return True
            else:
                return False
        except Exception as e:
            print("Error! in is_it_joomla: " + str(e))

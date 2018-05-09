#!/usr/bin/env python3

import skim_writer_io


class SkimCmsFilter:

    def is_it_drupal(self, url, headers: str, content: str) -> bool:
        '''
        Parse http response data for Drupal CMS
        '''
        try:
            writer = skim_writer_io.Skim_writer_io().writer
            check = str(headers) + str(content)
            if ("drupal" in check) or ("Drupal" in check):
                writer(url, "drupal")
                return True
        except Exception as e:
            print("Error! in drupal: " + str(e))

    def is_it_wordpress(self, url: str, headers: str) -> bool:
        '''
        Parse http response data for Wordpress CMS
        '''
        try:
            writer = skim_writer_io.Skim_writer_io().writer
            headers = str(headers)
            if ("wp" in headers) or ("xmlrpc.php" in headers):
                writer(url, "wordpress")
                return True
        except Exception as e:
            print("Error! in is_it_wordpress " + str(e))

    def is_it_sharepoint(self, url: str, headers: str) -> bool:
        '''
        Parse http response data for Sharepoint
        '''
        try:
            writer = skim_writer_io.Skim_writer_io().writer
            if (("MicrosoftSharePointTeamServices" in headers)
            or ("access-keys-sharepoint-schools.html" in headers)):
                writer(url, "sharepoint")
                return True
        except Exception as e:
            print("Error! in is_it_sharepoint: " + str(e))

    def is_it_joomla(self, url: str, headers: str) -> bool:
        '''
        Parse http response data for Joomla CMS
        '''
        try:
            writer = skim_writer_io.Skim_writer_io().writer
            if "joom" in str(headers):
                writer(url, "joomla")
                return True
            else:
                return False
        except Exception as e:
            print("Error! in is_it_joomla: " + str(e))




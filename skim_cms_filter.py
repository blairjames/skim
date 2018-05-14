#!/usr/bin/env python3

import skim_writer_io
from time import perf_counter as pc


class SkimCmsFilter:

    def __init__(self):
        self.perf_is_it_drupal: str = "n/a"
        self.perf_is_it_wordpress: str = "n/a"
        self.perf_is_it_sharepoint: str = "n/a"
        self.perf_is_it_joomla: str = "n/a"

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
                timer = str(p2 - p1)
                timer = timer[:8]
                self.perf_is_it_drupal = str(timer)
                return True
            else:
                p2 = pc()
                timer = str(p2 - p1)
                timer = timer[:8]
                self.perf_is_it_drupal = str(timer)
                return False
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
                timer = str(p2 - p1)
                timer = timer[:8]
                self.perf_is_it_wordpress = str(timer)
                return True
            else:
                p2 = pc()
                timer = str(p2 - p1)
                timer = timer[:8]
                self.perf_is_it_wordpress = str(timer)
                return False
        except Exception as e:
            print("Error! in is_it_wordpress " + str(e))

    def is_it_sharepoint(self, url: str, headers: str) -> bool:
        '''
        Parse http response data for Sharepoint
        '''
        try:
            p1 = pc()
            writer = skim_writer_io.Skim_writer_io().writer
            if any("SharePoint" in x for x in headers):
                writer(url, "sharepoint")
                p2 = pc()
                timer = str(p2 - p1)
                timer = timer[:8]
                self.perf_is_it_sharepoint = str(timer)
                return True
            else:
                p2 = pc()
                timer = str(p2 - p1)
                timer = timer[:8]
                self.perf_is_it_sharepoint = str(timer)
                return False
        except Exception as e:
            print("Error! in is_it_sharepoint: " + str(e))

    def is_it_joomla(self, url: str, headers: str, content: str) -> bool:
        '''
        Parse http response data for Joomla CMS
        '''
        try:
            p1 = pc()
            writer = skim_writer_io.Skim_writer_io().writer
            search_space = str("".join(headers)) + str(content)
            print("\n\n\n\n^^^^^^^^^^^^^^^^^^^^^^^^^^" + search_space)
            if "joomla" in search_space:
                writer(url, "joomla")
                p2 = pc()
                timer = str(p2 - p1)
                timer = timer[:8]
                self.perf_is_it_joomla = str(timer)
                return True
            else:
                p2 = pc()
                timer = str(p2 - p1)
                timer = timer[:8]
                self.perf_is_it_joomla = str(timer)
                return False
        except Exception as e:
            print("Error! in is_it_joomla: " + str(e))

#!/usr/bin/env python3

from typing import List
import toolbag
import skim_conf
import skim_utils
import skim_writer_io
import time


class SkimReader:
    '''
    Handle FileIO reads, reading from disks to lists.
    '''

    def fetch_domain_list(self, dir: str) -> List:
        '''
        Get the list of domains to scan, from file.
        Filter through the whitelist_sieve.
        Shuffle and return clean list
        '''
        try:
            url_list = []
            shuf = toolbag.Toolbag().shuffler
            dir = str(dir)
            apd = url_list.append
            lint = skim_utils.SkimUitls().lint
            with open(dir, "r") as url_file:
                for url in url_file.read().splitlines():
                    apd("http://" + str(url))
                url_file.close()
            col = toolbag.Toolbag().color
            lint(col("\nNumber of domains before whitelisting: " + str(len(url_list)), "yellow"))
            time.sleep(1.5)
            clean_list = self.whitelist_sieve(url_list)
            clean_list = shuf(clean_list)
            lint(col("Number of domains after whitelisting:  " + str(len(clean_list)), "yellow") + "\n\n")
            time.sleep(1.5)
            return clean_list
        except Exception as e:
            print("Error! in SkimController.fetch_domain_list: " + str(e))

    def whitelist_sieve(self, raw_master_list: List) -> List:
        '''
        Filter whitelisted domains from the list of urls to be processed
        '''
        try:
            whitelist = skim_conf.Skim_conf().whitelist_domains()
            writer = skim_writer_io.Skim_writer_io().writer
            clean_master_list = []
            apend = clean_master_list.append
            in_whitelist = False
            for url in raw_master_list:
                url = str(url)
                for white in whitelist:
                    white = str(white)
                    if white in url:
                        writer(url, "whitelisted")
                        in_whitelist = True
                    if in_whitelist == True:
                        break
                if in_whitelist == True:
                    in_whitelist = False
                    continue
                else:
                    if url not in clean_master_list:
                        apend(url)
            return clean_master_list
        except Exception as e:
            print("Error! in SkimController.whitelist_sieve: " + str(e))



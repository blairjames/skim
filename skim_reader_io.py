#!/usr/bin/env python3

from typing import List
import toolbag
import skim_conf
import skim_utils
import skim_writer_io


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
            with open(dir, "r") as url_file:
                for url in url_file.read().splitlines():
                    apd("http://" + str(url))
                url_file.close()
            clean_list = self.whitelist_sieve(url_list)
            clean_list = shuf(clean_list)
            return clean_list
        except Exception as e:
            print("Error! in SkimController.fetch_domain_list: " + str(e))

    def whitelist_sieve(self, raw_master_list) -> List:
        '''
        Filter whitelisted domains from the list of urls to be processed
        '''
        try:
            whitelist = skim_conf.Skim_conf().whitelist_domains()
            writer = skim_writer_io.Skim_writer_io().writer
            lint = skim_utils.SkimUitls().lint
            clean_master_list = []
            apd = clean_master_list.append
            for url in raw_master_list:
                url = str(url)
                for white in whitelist:
                    white = str(white)
                    if white in url:
                        writer(url, "whitelisted")
                    else:
                        apd(url)
            return clean_master_list
        except Exception as e:
            print("Error! in SkimController.whitelist_sieve: " + str(e))



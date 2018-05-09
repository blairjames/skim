#!/usr/bin/env python3

import time

import multiprocessing
import random
import skim_cleaner
import skim_conf
import skim_hasher
import skim_preparation
import skim_reader_io
import skim_requester
import skim_utils
import skim_writer_io
import toolbag


class SkimController:

    def __init__(self):
        ''' Controller Constructor - Set instance attributes here '''
        try:
            self.processes: int = 256
            self.http_timeout: int = 60
            self.staggering: int = 30
            self.num_domains: int = 0
            self.basepath:str = "/root/scripts/skim/output/"
            self.path_to_urls: str = "/root/scripts/skim/master_list_external_domains.txt"
            self.logfile: str = (self.basepath + "log_sites.txt")
            self.tb = toolbag.Toolbag()
            self.writer = skim_writer_io.Skim_writer_io().writer
            self.conf = skim_conf.Skim_conf()
            self.requester = skim_requester.SkimRequester()
            self.hasher = skim_hasher.Hasher()
            self.prep = skim_preparation.Skim_preparation()
            self.utils = skim_utils.SkimUitls()
            self.reader = skim_reader_io.SkimReader().fetch_domain_list
            self.lint = self.utils.lint
            self.clean = skim_cleaner.SkimCleaner()
        except Exception as e:
            print("Error! in SkimController.constructor: " + str(e))

    def clean_and_print_banner(self) -> bool:
        '''
        clean up and print the banner.
        '''
        try:
            self.utils.remove_orphan_files(self.basepath)
            self.tb.clear_screen()
            self.conf.show_banner()
            return True
        except Exception as e:
            print("Error! in SkimController.clean_and_print_banner: " + str(e))

    def is_internet_available(self) -> bool:
        '''
        Check that internet connectivity is available.
        '''
        try:
            if self.utils.test_internet():
                return True
            else:
                return False
        except Exception as e:
            print("Error! in SkimController.is_internet_available: " + str(e))


    def parallelize(self, clean_master_list) -> bool:
        '''
        Generate a Pool of processes, then map the elements in the domain list to the director function
        '''
        try:
            with multiprocessing.Pool(int(self.processes), maxtasksperchild=10) as pool:
                pool.map(self.director, clean_master_list)
            return True
        except AssertionError as i:
            print("Error!! in SkimController.parallelize multi processing map: " + str(i))

    def director(self, url: str) -> bool:
        '''
        Enforce staggering for race safety then send to http requester
        '''
        try:
            wait = random.randint(0, int(self.staggering))
            time.sleep(int(wait))
            self.requester.send_request(url)
            return True
        except Exception as e:
            self.lint("Error! in SkimController.director method: " + str(e))

    def display_results(self) -> bool:
        '''
        Display the results and move the files into their own folder
        '''
        self.clean.print_counts()
        self.clean.move_files("/root/scripts/skim/output/")
        return True


def main():
    '''
    Execution flow is controlled from here.
    '''
    controller = SkimController()
    if not controller.is_internet_available:
        controller.lint("\nError! - Check internet connectivity\n")
        exit(1)
    else:
        controller.clean_and_print_banner()
        list_of_domains = controller.reader(controller.path_to_urls)
        controller.parallelize(list_of_domains)
    return True


if __name__ == '__main__':
    main()
#!/usr/bin/env python3

import skim_utils

#TODO: Get web server version and CVE check.
#wpscan etc


class SkimController:
    '''
    This is the Driver Class, it's instantiation in the main() drives execution of the application.
    '''
    def __init__(self):
        '''
        Controller Constructor - Set instance attributes here.
        '''
        try:
            self.processes: int = 32
            self.http_timeout: int = 60
            self.staggering: int = 20
            self.basepath:str = "/opt/skim/output/"
            self.path_to_urls = "/opt/skim/master_list_external_domains.txt"
            self.logfile: str = (self.basepath + "log.txt")

        except Exception as e:
            print("Error! in SkimController.constructor: " + str(e))

    def clean_and_print_banner(self) -> bool:
        '''
        clean up and print the banner.
        '''
        try:
            import toolbag
            import skim_conf
            utils = skim_utils.SkimUitls()
            conf = skim_conf.Skim_conf()
            tb = toolbag.Toolbag()
            utils.remove_orphan_files(self.basepath)
            tb.clear_screen()
            conf.show_banner()
            return True
        except Exception as e:
            print("Error! in SkimController.clean_and_print_banner: " + str(e))

    def is_internet_available(self) -> bool:
        '''
        Check that internet connectivity is available.
        '''
        try:
            utils = skim_utils.SkimUitls()
            if utils.test_internet():
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
            import multiprocessing
            with multiprocessing.Pool(int(self.processes), maxtasksperchild=40) as pool:
                pool.map(self.director, clean_master_list)
            return True
        except AssertionError as i:
            print("Error!! in SkimController.parallelize multi processing map: " + str(i))

    def director(self, url):
        '''
        Enforce staggering to avoid link flooding, then send to http requester.
        '''
        try:
            import random
            import time
            import skim_requester
            requester = skim_requester.SkimRequester()
            wait = random.randint(0, int(self.staggering))
            time.sleep(int(wait))
            requester.send_request(url)
        except Exception as e:
            print("Error! in SkimController.director method: " + str(e))

    def display_results(self) -> bool:
        '''
        Display the results and move the files into their own folder
        '''
        try:
            import skim_cleaner
            clean = skim_cleaner.SkimCleaner()
            clean.print_counts()
            clean.move_files("/opt/skim/output/")
            return True
        except Exception as e:
            print("Error! in SkimController.display_results: " + str(e))

    def does_everything_exist(self) -> bool:
        '''
        check dirs and files exists, if not create them.
        '''
        try:
            util = skim_utils.SkimUitls()
            print(str(self.basepath))
            print(self.path_to_urls)
            print(str(self.logfile))
            base = util.check_dir_exists(self.basepath)
            print(str(base))
            urls = util.check_file_exists(self.path_to_urls)
            print(str(urls))
            log = util.check_file_exists(self.logfile)
            print(str(log))
            if not base or not urls or not log:
                raise IOError
            else:
                return True
        except IOError as i:
            print("IO Error! - controller.does_everything_exist.Checking_files_creating_if_not_exists: " + str(i))
        except Exception as e:
            print("Error! - controller.does_everything_exist: " + str(e))


def main():
    '''
    Execution flow is controlled from here.
    '''
    controller = SkimController()
    lint = skim_utils.SkimUitls().lint
    if not controller.is_internet_available:
        lint("\nError! - Check internet connectivity\n")
        exit(1)
    #check dirs and files exists, if not create them.
    if not controller.does_everything_exist():
        lint("\nIO Error! - File does not exist.")
        exit(1)
    else:
        import skim_reader_io
        reader = skim_reader_io.SkimReader().fetch_domain_list
        controller.clean_and_print_banner()
        list_of_domains = reader(controller.path_to_urls)
        controller.parallelize(list_of_domains)

if __name__ == '__main__':
    main()


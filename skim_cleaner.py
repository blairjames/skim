#!/usr/bin/env python3


class SkimCleaner:

    def move_files(self, path):
        '''
        Move files from each pass into their own timestamp directory.
        '''
        try:
            import subprocess
            import toolbag
            tb = toolbag.Toolbag()
            path = str(path)
            ts = tb.create_timestamp()
            ts = str(ts)
            destpath = (path + ts)
            if tb.check_dir_exists(destpath):
                mv = subprocess.run(["/bin/mv " + path + "/*.txt " + destpath + "/"],
                            stdout=subprocess.PIPE, shell=True)
                if mv.returncode != 0:
                    raise Exception
            else:
                raise Exception
        except Exception as e:
            mess = "Error! in Cleaner.move_files() : " + str(e)
            mess = str(mess)
            print(mess)

    def count_sites(self, filename):
        '''
        Return number of lines in filename
        '''
        try:
            import skim_controller
            import os
            basepath: str = skim_controller.SkimController().basepath
            fullpath = str(basepath) + str(filename)
            if not os.path.isfile(fullpath):
                return "None discovered."
            with open(fullpath, "r") as file:
                lines = file.readlines()
                wc = len(lines)
                return str(wc)
        except Exception as e:
            print("Error!! in Cleaner.count_sites(): " + str(e))

    def print_counts(self):
        '''
        Print the number of sites in each category
        '''
        try:
            import skim_controller
            import skim_utils
            num_domains: int = skim_controller.SkimController().num_domains
            lint = skim_utils.SkimUitls().lint
            lint("\n***************************************************************")
            lint("Total Sites: " + str(num_domains))
            lint("Sites up: " + str(self.count_sites("up.txt")))
            lint("Sites not responding: " + str(self.count_sites("not_responding.txt")))
            lint("Sharepoint Sites: " + str(self.count_sites("sharepoint.txt")))
            lint("Wordpress Sites: " + str(self.count_sites("wordpress.txt")))
            lint("Drupal Sites: " + str(self.count_sites("drupal.txt")))
            lint("***************************************************************")
        except Exception as e:
            print("Error! in Cleaner.print_counts(): " + str(e))




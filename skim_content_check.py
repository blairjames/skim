#!/usr/bin/env python3

import skim_utils
import subprocess
from time import perf_counter as pc
from typing import List, Dict


class SkimContentCheck:
    '''
    Once all sites have been processed, we take the current list of content hashes
    and compare them to the relevant hashes from the last pass to detect any changes.
    If the hashes of a site do not match we take the current content and compare to
    the content from the last pass to indicate exactly what was modified.
    These details are them emailed as an alert for further investigation.
    '''
    def __init__(self):
        self.perf_get_hash_results = pc
        self.perf_get_dir_name_cmd_builder = pc
        self.perf_get_dir_name = pc
        self.perf_get_file_name = pc
        self.perf_compare_hashes = pc
        self.perf_get_content = pc
        self.perf_search_content = pc


    def get_hash_results(self, path: str) -> Dict:
        '''
        Read hash file from disk to Dictionary.
        Split the URL and hash_digest using "~" as delimiter, return tuple and map URL to hash in Dict.
        '''
        try:
            p1 = pc()
            hash_dict: Dict = {}
            print("\n\nget_hash_results file to open: " + str(path))
            path = str(path.rstrip("\n"))
            with open(path, "r") as file:
                for line in file.readlines():
                    site, content_hash = line.split("~")
                    hash_dict[str(site)] = str(content_hash)
            file.close()
            p2 = pc()
            self.perf_get_hash_results = p2 - p1
            return hash_dict
        except Exception as e:
            print("Error! in SkimContentCheck.get_hash_results: " + str(e))

    def get_dir_name_cmd_builder(self, which_results: str) -> str:
        '''
        Return a command string to be run by "get_dir_name" according to the "which_results" parameter.
        '''
        try:
            p1 = pc()
            import skim_controller
            basepath: str = skim_controller.SkimController().basepath
            cmd1 = "ls -td " + str(basepath) + "201* | head -n 1"
            cmd2 = "ls -td " + str(basepath) + "201* | head -n 2 | tail -n 1"
            if which_results == "most_recent":
                p2 = pc()
                self.perf_get_dir_name_cmd_builder = p2 - p1
                return str(cmd1)
            elif which_results == "second":
                p2 = pc()
                self.perf_get_dir_name_cmd_builder = p2 - p1
                return str(cmd2)
        except Exception as e:
            print("Error! in SkimContentCheck.get_dir_name_cmd_builder: " + str(e))

    def get_dir_name(self, cmd: str) -> str:
        '''
        Return the name of the directory after running the "cmd" parameter.
        '''
        try:
            p1 = pc()
            lint = skim_utils.SkimUitls().lint
            lint("CMD for file name: " + str(cmd))
            dir_name = subprocess.run([str(cmd)], stdout = subprocess.PIPE, shell = True)
            if dir_name.returncode != 0:
                raise IOError
            dir_out = dir_name.stdout
            dir_out = dir_out.decode("utf-8")
            dir_out = dir_out.rstrip('\n')
            lint(str(dir_out))
            p2 = pc()
            self.perf_get_dir_name = p2 - p1
            return str(dir_out)
        except IOError as i:
            print("get_file_path_subprocess IOERROR" + str(i))
        except Exception as e:
            print("get_file_path" + str(e))

    def get_file_name(self, dir_name: str, file_to_return: str) -> str:
        '''
        Return the name of the hash file in the directory calculated by get_dir_name
        '''
        try:
            p1 = pc()
            lint = skim_utils.SkimUitls().lint
            file_cmd = ("ls -td " + str(dir_name) + "/*" + str(file_to_return) + "*")
            lint("File cmd: " + str(file_cmd))
            file_name = subprocess.run([str(file_cmd)], stdout = subprocess.PIPE, shell = True)
            if file_name.returncode != 0:
                raise IOError
            file_name_out = file_name.stdout
            file_name_out = file_name_out.decode("utf-8")
            lint("File name: " + str(file_name_out))
            p2 = pc()
            self.perf_get_file_name = p2 - p1
            return str(file_name_out)
        except IOError as i:
            print("Error! in content.checker.get_hashes: IOERROR subprocess: " + str(i))
        except Exception as e:
            print("Error! in content.checker.get_hashes: " + str(e))

    def compare_hashes(self, dict1: Dict, dict2: Dict) -> List:
        '''
        Use URLs as keys, get corresponding hash from both dictionaries and compare.
        Return List of URL's with non matching hashes.
        '''
        try:
            p1 = pc()
            lint = skim_utils.SkimUitls().lint
            mismatches = []
            apd = mismatches.append
            for key in dict1.keys():
                hash_latest = dict1.get(key)
                hash_second = dict2.get(key)
                if (not hash_latest) or (not hash_second):
                    continue
                if (hash_latest != hash_second):
                    lint("ALERT!! - Content has changed on: " + str(key) + "\n")
                    lint(str(key))
                    lint(str(hash_latest))
                    lint(str(hash_second))
                    apd(str(key))
                else:
                    continue
                p2 = pc()
                self.perf_compare_hashes = p2 -p1
                return mismatches
        except Exception as e:
            print("Error! in compare_hashes: " + str(e))

    def get_content(self, file_name: str) -> List:
        '''
        Read content file into List
        '''
        try:
            p1 = pc()
            content = []
            apd = content.append
            with open(file_name.rstrip("\n"), "r") as file:
                for line in file.readlines():
                    apd(line)
                file.close()
                p2 = pc()
                self.perf_get_content = p2 - p1
            return content
        except Exception as e:
            print("Error! in SkimContentCheck.get_content: " + str(e))

    def search_content(self, domain: str, content_list: List) -> List:
        '''
        Find and retrieve domain specific content from List
        '''
        try:
            p1 = pc()
            starter = ("$$$$$$$$$$~~~~~~~~~~$$$$$$$$$$" + str(domain) +
                       "$$$$$$$$$$~~~~~~~~~~$$$$$$$$$$").rstrip("\n").rstrip(" ")
            ender = ("%%%%%%%%%%~~~~~~~~~~~%%%%%%%%%%" + str(domain) +
                     "%%%%%%%%%%~~~~~~~~~~~%%%%%%%%%%").rstrip("\n").rstrip(" ")
            site_content = []
            apnd = site_content.append
            i = int(0)
            write_flag = False
            while i < len(content_list):
                if write_flag == False:
                    if starter in content_list[i]:
                        write_flag = True
                if write_flag == True:
                    apnd(content_list[i])
                    i += 1
                    if ender in content_list[i]:
                        break
                else:
                    i += 1
            p2 = pc()
            self.perf_search_content = p2 - p1
            return site_content
        except Exception as e:
            print("Error! in SkimContentCheck.get_content: " + str(e))

    def print_perf_values(self):
        '''
        Display performance timings for each method
        '''
        import skim_cms_filter
        cms = skim_cms_filter.SkimCmsFilter()
        lint = skim_utils.SkimUitls().lint
        lint(
        "\nperf_get_hash_results: " + str(self.perf_get_hash_results) +
        "\nperf_get_dir_name_cmd_builder: " + str(self.perf_get_dir_name_cmd_builder) +
        "\nperf_get_dir_name: " + str(self.perf_get_dir_name) +
        "\nperf_get_file_name: " + str(self.perf_get_file_name) +
        "\nperf_compare_hashes: " + str(self.perf_compare_hashes) +
        "\nperf_get_content: " + str(self.perf_get_content) +
        "\nperf_search_content: " + str(self.perf_search_content) +
        "\nperf_is_it_wordpress: " + str(cms.perf_is_it_wordpress) +
        "\nperf_is_it_sharepoint: " + str(cms.perf_is_it_sharepoint) +
        "\nperf_is_it_joomla: " + str(cms.perf_is_it_joomla))


def main():
    '''
    Content checking execution flow is driven from here.
    '''
    try:
        lint = skim_utils.SkimUitls().lint
        check = SkimContentCheck()

        most_recent = check.get_dir_name_cmd_builder("most_recent")
        second = check.get_dir_name_cmd_builder("second")

        most_recent_dir = check.get_dir_name(most_recent)
        second_dir = check.get_dir_name(second)

        last_hash_results_file_name = check.get_file_name(most_recent_dir, "hash")
        second_last_hash_results_file_name = check.get_file_name(second_dir, "hash")

        last_content_file_name = check.get_file_name(most_recent_dir, "content")
        second_last_content_file_name = check.get_file_name(second_dir, "content")

        latest_hash_results = check.get_hash_results(last_hash_results_file_name)
        second_last_hash_results = check.get_hash_results(second_last_hash_results_file_name)

        lint("\nlast_hash_results_file_name: " + str(last_hash_results_file_name) +
              " Number of results: " + str(len(latest_hash_results)))

        lint("\nsecond_last_hash_results_file_name: " + str(second_last_hash_results_file_name) +
              " Number of results: " + str(len(second_last_hash_results)))

        lint("\nlast_content_file_name: " + str(last_content_file_name))
        lint("\nsecond_last_content_file_name: " + str(second_last_content_file_name))

        mismatches = check.compare_hashes(latest_hash_results, second_last_hash_results)
        if not mismatches:
            lint("\nAll urls have matching hash.\n")
        else:
            for domain in mismatches:
                last_content_list = check.get_content(last_content_file_name)
                second_last_content_list = check.get_content(second_last_content_file_name)
                cont_last = check.search_content(domain, last_content_list)
                cont_second = check.search_content(domain, second_last_content_list)
                diff = list(set(cont_second) ^ set(cont_last))
                df = "\n".join(diff)

                import gmail
                import toolbag
                col = toolbag.Toolbag().color
                log_mess = col("\nContent Warning - " + str(domain) + "\nThese elements are different:\n", "red")
                lint("\n" + log_mess + "\n" + col(df, "yellow"))
                mail_mess = "Content Warning - " + str(domain)
                gmail.Gmail().sendText(mail_mess, df)
                lint("\n\nPerformance Timings per method:")
                lint(str(check.print_perf_values()))

    except Exception as e:
        print("Error! in content_checker.main(): " + str(e))


if __name__ == '__main__':
    main()



#!/usr/bin/env python3

import time

import det_gmail
import skim_controller
import skim_utils
import subprocess
import toolbag
from typing import List, Dict


class SkimContentCheck:
    '''
    Once all sites have been processed, we take the current list of content hashes
    and compare them to the relevant hashes from the last pass to detect any changes.
    If the hashes of a site do not match we take the current content and compare to
    the content from the last pass to indicate exactly what was modified.
    These details are them emailed as an alert for further investigation.
    '''

    def get_hash_results(self, path: str):
        '''
        Read hash file from disk to Dictionary.
        Split the URL and hash_digest using "~" as delimiter, return tuple and map URL to hash in Dict.
        '''
        try:
            hash_dict: Dict = {}
            print("get_hash_results file to open: " + str(path))
            path = str(path.rstrip("\n"))
            with open(path, "r") as file:
                for line in file.readlines():
                    site, content_hash = line.split("~")
                    hash_dict[str(site)] = str(content_hash)
            file.close()
            return hash_dict
        except Exception as e:
            print("get_hash_results" + str(e))

    def get_dir_name_cmd_builder(self, which_results: str):
        '''
        Return a command string to be run by "get_dir_name" according to the "which_results" parameter.
        '''
        try:
            basepath: str = skim_controller.SkimController().basepath
            cmd1 = "ls -td " + str(basepath) + "/*/ | head -n 1"
            cmd2 = "ls -td " + str(basepath) + "/*/ | head -n 2 | tail -n 1"
            if which_results == "most_recent":
                return str(cmd1)
            elif which_results == "second":
                return str(cmd2)
        except Exception as e:
            print("Error! in SkimContentCheck.get_dir_name_cmd_builder: " + str(e))

    def get_dir_name(self, cmd):
        '''
        Return the name of the directory after running the "cmd" parameter.
        '''
        try:
            lint = skim_utils.SkimUitls().lint
            lint("CMD for file name: " + str(cmd))
            dir_name = subprocess.run([str(cmd)], stdout = subprocess.PIPE, shell = True)
            if dir_name.returncode != 0:
                raise IOError
            dir_out = dir_name.stdout
            dir_out = dir_out.decode("utf-8")
            dir_out = dir_out.rstrip('\n')
            lint(str(dir_out))
            return str(dir_out)
        except IOError as i:
            print("get_file_path_subprocess IOERROR" + str(i))
        except Exception as e:
            print("get_file_path" + str(e))

    def get_hash_file_name(self, dir_name):
        '''
        Return the name of the hash file in the directory calculated by get_dir_name
        '''
        try:
            lint = skim_utils.SkimUitls().lint
            color = toolbag.Toolbag().color
            file_cmd = ("ls -td " + str(dir_name) + "*hash*")
            lint("File cmd: " + str(file_cmd))
            file_name = subprocess.run([str(file_cmd)], stdout = subprocess.PIPE, shell = True)
            if file_name.returncode != 0:
                raise IOError
            file_name_out = file_name.stdout
            file_name_out = file_name_out.decode("utf-8")
            lint(color("File name: " + str(file_name_out), "yellow"))
            return str(file_name_out)
        except IOError as i:
            print("Error! in content.checker.get_hashes: IOERROR subprocess: " + str(i))
        except Exception as e:
            print("Error! in content.checker.get_hashes: " + str(e))

    def compare_hashes(self, dict1, dict2) -> List:
        '''
        Use URLs as keys, get corresponding hash from both dictionaries and compare.
        Return List of URL's with non matching hashes.
        '''
        try:
            lint = skim_utils.SkimUitls().lint
            mismatches = []
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
                    mismatches.append(str(key))
                else:
                    continue
                return mismatches
        except Exception as e:
            print("Error! in compare_hashes: " + str(e))

def main():
    try:
        check = SkimContentCheck()
        tb = toolbag.Toolbag()
        last_results_path = check.get_hash_file_name(check.get_dir_name("most_recent"))
        second_last_results_path = check.get_hash_file_name(check.get_dir_name("second"))
        latest_results = check.get_hash_results(last_results_path)
        len = latest_results.__len__()
        print(tb.color("Number of hash results: " + str(len), "yellow"))

        second_last_results = check.get_hash_results(second_last_results_path)
        seclen = second_last_results.__len__()
        print(tb.color("Number of hash results: " + str(seclen), "yellow"))

        comp = check.compare_hashes(latest_results, second_last_results)
        if comp.__len__() < 1:
            print(tb.color("\nAll urls have matching hash.\n", "green"))
            exit(0)
        else:
            for url in comp:
                iurl = str(url)
                first, firsthash = check.processor(iurl)
                print("\nFetching content from: " + str(iurl) + "\nHash: " +
                      str(firsthash) + "\n\nFetching new content and hashing...")
                time.sleep(1)
                second, sechash = check.processor(iurl)
                print("Hash: " + str(sechash))

                diff_file_1 = "/root/scripts/skim/skim_content.diff"
                diff_file_2 = "/root/scripts/skim/skim_content2.diff"

                with open(diff_file_1, "w") as filea:
                    filea.write(str(first))

                with open(diff_file_2, "w") as fileb:
                    fileb.write(str(second))

                diff = subprocess.run(["/usr/bin/diff", diff_file_1, diff_file_2], stdout=subprocess.PIPE)
                out = diff.stdout
                out = out.decode()

                if not out:
                    print("\nNo Difference!")
                else:
                    det_gmail.Gmail().sendText("Difference in site content: " + iurl, str(out))
                    print("\nDifference in site content: \n" + str(out))
        return True

    except Exception as e:
        print("Error! in content_checker.main(): " + str(e))


if __name__ == '__main__':
    main()



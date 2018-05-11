#!/usr/bin/env python3

import skim_utils
import subprocess
from typing import List, Dict


class SkimContentCheck:
    '''
    Once all sites have been processed, we take the current list of content hashes
    and compare them to the relevant hashes from the last pass to detect any changes.
    If the hashes of a site do not match we take the current content and compare to
    the content from the last pass to indicate exactly what was modified.
    These details are them emailed as an alert for further investigation.
    '''

    def get_hash_results(self, path: str) -> Dict:
        '''
        Read hash file from disk to Dictionary.
        Split the URL and hash_digest using "~" as delimiter, return tuple and map URL to hash in Dict.
        '''
        try:
            print("\n\nIn get hash results")
            hash_dict: Dict = {}
            print("\n\nget_hash_results file to open: " + str(path))
            path = str(path.rstrip("\n"))
            with open(path, "r") as file:
                for line in file.readlines():
                    print("\n\nSplitting: " + str(line))
                    site, content_hash = line.split("~")
                    hash_dict[str(site)] = str(content_hash)
                    print("\n\nAfter split into dict: "  + str(site) + " " + str(content_hash))
            file.close()
            return hash_dict
        except Exception as e:
            print("Error! in SkimContentCheck.get_hash_results: " + str(e))

    def get_dir_name_cmd_builder(self, which_results: str) -> str:
        '''
        Return a command string to be run by "get_dir_name" according to the "which_results" parameter.
        '''
        try:
            import skim_controller
            basepath: str = skim_controller.SkimController().basepath
            cmd1 = "ls -td " + str(basepath) + "201* | head -n 1"
            cmd2 = "ls -td " + str(basepath) + "201* | head -n 2 | tail -n 1"
            if which_results == "most_recent":
                return str(cmd1)
            elif which_results == "second":
                return str(cmd2)
        except Exception as e:
            print("Error! in SkimContentCheck.get_dir_name_cmd_builder: " + str(e))

    def get_dir_name(self, cmd: str) -> str:
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

    def get_file_name(self, dir_name: str, file_to_return: str) -> str:
        '''
        Return the name of the hash file in the directory calculated by get_dir_name
        '''
        try:
            lint = skim_utils.SkimUitls().lint
            file_cmd = ("ls -td " + str(dir_name) + "/*" + str(file_to_return) + "*")
            lint("File cmd: " + str(file_cmd))
            file_name = subprocess.run([str(file_cmd)], stdout = subprocess.PIPE, shell = True)
            if file_name.returncode != 0:
                raise IOError
            file_name_out = file_name.stdout
            file_name_out = file_name_out.decode("utf-8")
            lint("File name: " + str(file_name_out))
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
            lint = skim_utils.SkimUitls().lint
            mismatches = []
            apd = mismatches.append
            for key in dict1.keys():
                hash_latest = dict1.get(key)
                hash_second = dict2.get(key)
                lint("Latest Hash: " + str(hash_latest))
                lint("Second Hash: " + str(hash_second))
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
                return mismatches
        except Exception as e:
            print("Error! in compare_hashes: " + str(e))

    def get_content(self, file_name: str) -> List:
        '''
        Read content file into List
        '''
        try:
            content = []
            apd = content.append
            with open(file_name, "r") as file:
                for line in file.readlines():
                    apd(line)
                file.close()
            return content
        except Exception as e:
            print("Error! in SkimContentCheck.get_content: " + str(e))

    def search_content(self, domain: str, content_list: List) -> str:
        '''
        Find and retrieve domain specific content from List
        '''
        try:
            output = []
            apd = output.append
            index_start = content_list.index\
               ("$$$$$$$$$$~~~~~~~~~~$$$$$$$$$$" + str(domain) + "$$$$$$$$$$~~~~~~~~~~$$$$$$$$$$")
            index_end = content_list.index\
               ("%%%%%%%%%%~~~~~~~~~~~%%%%%%%%%%" + str(domain) + "%%%%%%%%%%~~~~~~~~~~~%%%%%%%%%%")

            i = int(index_start)
            print("Index Start: " + str(index_start))
            print("Index end: " + str(index_end))
            while i < int(index_end):
                apd(content_list[i])
                i += 1
            output = "".join(output).rstrip("\n").lstrip(" ")
            print(str(output))
            return str(output)
        except Exception as e:
            print("Error! in SkimContentCheck.get_content: " + str(e))


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
            exit(0)
        else:
            for domain in mismatches:
                last_content_list = check.get_content(last_content_file_name)
                second_last_content_list = check.get_content(second_last_content_file_name)

                cont_last = check.search_content(domain, last_content_list)
                cont_second = check.search_content(domain, second_last_content_list)

                diff_file_1 = "/root/scripts/skim/skim_content.diff"
                diff_file_2 = "/root/scripts/skim/skim_content2.diff"

                with open(diff_file_1, "w") as filea:
                    filea.write(str(cont_last))
                with open(diff_file_2, "w") as fileb:
                    fileb.write(str(cont_second))

                diff = subprocess.run(["/usr/bin/diff", diff_file_1, diff_file_2], stdout=subprocess.PIPE)
                out = diff.stdout
                out = out.decode()

                if not out:
                    lint("\nNo Difference!")
                else:
                    import det_gmail
                    message = "Difference in site content: " + str(domain) + "\n" + str(out)
                    det_gmail.Gmail().sendText("Content Modification Warning.", message)
                    lint(message)


    except Exception as e:
        print("Error! in content_checker.main(): " + str(e))


if __name__ == '__main__':
    main()



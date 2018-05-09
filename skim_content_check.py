#!/usr/bin/env python3

import time

import det_gmail
import hashlib
import requests
import skim_hasher
import skim_controller
import skim_utils
import subprocess
import toolbag


class SkimContentCheck:
    '''
    Once all sites have been processed, we take the current list of content hashes
    and compare them to the relevant hashes from the last pass to detect any changes.
    If the hashes of a site do not match we take the current content and compare to
    the content from the last pass to indicate exactly what was modified.
    These details are them emailed as an alert for further investigation.
    '''

    def get_hash_results(self, path):
        '''
        Read hash file from disk to Dictionary.
        Split the URL and hash_digest using "~" as delimiter, return tuple and map URL to hash in Dict.
        '''
        try:
            hash_dict = {}
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

    def get_file_path(self, which_results):
        try:
            basepath = skim_controller.SkimController().basepath
            lint = skim_utils.SkimUitls().lint
            cmd1 = "ls -td " + str(basepath) + "/*/ | head -n 1"
            cmd2 = "ls -td " + str(basepath) + "/*/ | head -n 2 | tail -n 1"
            if which_results == "most_recent":
                cmd = str(cmd1)
            elif which_results == "second":
                cmd = str(cmd2)
            else:
                raise IOError
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

    def get_hash_file(self, dir_out):
        try:
            color = toolbag.Toolbag().color
            file_cmd = ("ls -td " + str(dir_out) + "*hash*")
            print("File cmd: " + str(file_cmd))
            file_name = subprocess.run([str(file_cmd)], stdout = subprocess.PIPE, shell = True)
            if file_name.returncode != 0:
                raise IOError
            file_name_out = file_name.stdout
            file_name_out = file_name_out.decode("utf-8")
            print(color("File name: " + str(file_name_out), "yellow"))
            return str(file_name_out)
        except IOError as i:
            print("Error! in content.checker.get_hashes: IOERROR subprocess: " + str(i))
        except Exception as e:
            print("Error! in content.checker.get_hashes: " + str(e))

    def compare_hashes(self, dict1, dict2):
        try:
            mismatches = []
            for key in dict1.keys():
                hash_latest = dict1.get(key)
                hash_second = dict2.get(key)
                if (not hash_latest) or (not hash_second):
                    continue
                if (hash_latest != hash_second):
                    print("ALERT!! - Content has changed on: " + str(key) + "\n")
                    print(str(key))
                    print(str(hash_latest))
                    print(str(hash_second))
                    mismatches.append(str(key))
                else:
                    continue
            if (len(mismatches) > 0):
                return mismatches
            else:
                return False
        except Exception as e:
            print("Error! in compare_hashes: " + str(e))

    def get_response(self, url):
        try:
            header = toolbag.Toolbag().get_headers
            res = requests.get(str(url), headers=header("ie"))
            cont = res.text
            cont = str(cont)
            return cont
        except Exception as e:
            print("Error in content_checker.get_response: " + str(e))




    #use the hasher one
    def checker(self, line):
        try:
            dynamic_content = skim_hasher.Hasher().dynamic_content
            line = str(line)
            for each in dynamic_content:
                if str(each) in str(line):
                    return True
            return False
        except Exception as e:
            print("Error! in content.checker.checker: ", str(e))



    def strip_digest(self, content):
        try:
            modded = []
            content = str(content)
            for line in content.splitlines():
                if not self.checker(line):
                    modded.append(str(line))
            if len(modded) > 0:
                return "\n".join(modded)
            else:
                return False
        except Exception as e:
            print("Error! in content.checker.strip_digest: " + str(e))

    def hashit(self, content):
        try:
            if not content:
                raise Exception
            encoded = content.encode("utf-8")
            md5 = hashlib.md5(encoded)
            md5d = md5.hexdigest()
            return str(md5d)
        except Exception as e:
            print("Error! in content_checker.hashit(): " + str(e))

    def processor(self, url):
        try:
            cont = self.get_response(str(url))
            processed = self.strip_digest(cont)
            hash = self.hashit(processed)
            return processed, hash
        except Exception as e:
            print("Error! in content.checker.processor: " + str(e))

def main():
    try:
        check = SkimContentCheck()
        check.tb.clear_screen()

        last_results_path = check.get_hash_file(check.get_file_path(check.basepath, "most_recent"))
        second_last_results_path = check.get_hash_file(check.get_file_path(check.basepath, "second"))

        latest_results = check.get_hash_results(last_results_path)
        len = latest_results.__len__()
        print(check.tb.color("Number of hash results: " + str(len), "yellow"))

        second_last_results = check.get_hash_results(second_last_results_path)
        seclen = second_last_results.__len__()
        print(check.tb.color("Number of hash results: " + str(seclen), "yellow"))

        comp = check.compare_hashes(latest_results, second_last_results)
        if not comp:
            print(check.tb.color("\nAll urls have matching hash.\n", "green"))
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

                diff_file_1 = "/root/scripts/skim/hash_tester1.txt"
                diff_file_2 = "/root/scripts/skim/hash_tester2.txt"

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



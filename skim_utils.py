#!/usr/bin/env python3

from time import perf_counter as pc


class SkimUitls:
    def __init__(self):
        self.perf_manage_content = pc

    def lint(self, message: str) -> bool:
        '''
        Log and print at the same time.
        '''
        try:
            import toolbag
            from skim_controller import SkimController
            message = str(message)
            ts = toolbag.Toolbag().create_timestamp()
            ts = str(ts)
            logfile = SkimController().logfile
            with open(logfile, "a") as file:
                file.write(ts + " : - " + message + "\n")
                file.close()
                print(message)
            return True
        except IOError as i:
            print("IO Error in SkimUitls.lint: " + str(i))
        except Exception as e:
            print("Error in SkimUitls.lint" + str(e))

    def check_file_exists(self, filename: str) -> bool:
        '''
        If filename parameter does not exist, create it.
        '''
        try:
            import os
            import subprocess
            file = str(filename)
            if (os.path.isfile(file)):
                return True
            else:
                tch = ("/bin/touch " + file)
                touch_file = subprocess.run([tch], stdin=subprocess.PIPE, stdout=subprocess.PIPE,
                                            stderr=subprocess.PIPE, shell=True)
                if "Permission" in str(touch_file.stderr):
                    raise AssertionError
                if touch_file.returncode != 0:
                    raise Exception
                return True
        except AssertionError as a:
            print("ERROR! - in check_file_exists Insufficient Permissions: " + str(a))
        except Exception as e:
            print("ERROR! - In \"check_file_exists\": " + str(e))

    def check_dir_exists(self, dir: str) -> bool:
        '''
        If directory parameter does not exist, create it.
        '''
        try:
            import os
            import subprocess
            if (os.path.isdir(str(dir))):
                return True
            else:
                cmd = ("/bin/mkdir " + str(dir))
                mkdir = subprocess.run([cmd], stdin=subprocess.PIPE, stdout=subprocess.PIPE,
                                       stderr=subprocess.PIPE, shell=True)
                if "Permission" in str(mkdir.stderr):
                    raise AssertionError
                if mkdir.returncode != 0:
                    raise Exception
                return True
        except AssertionError as a:
            print("ERROR! - Insufficient Permissions: " + str(a))
        except Exception as e:
            print("ERROR! - In \"check_dir_exists\": " + str(e))

    def how_many_domains_in_list(self, path_to_list: str):
        '''
        Count the number of lines in the domain list
        '''
        try:
            with open(str(path_to_list), "r") as file:
                lines = file.readlines()
                lc = len(lines)
                return str(lc)
        except Exception as e:
            print("Error! in SkimUitls.how_many_domains_in_list: " + str(e))

    def manage_content(self, url: str, content: str) -> bool:
        '''
        Take content from HTTP response, remove dynamic elements,
        store content and hash for comparison on next pass
        '''
        try:
            import skim_writer_io
            import skim_hasher
            writer = skim_writer_io.Skim_writer_io().writer
            h = skim_hasher.Hasher()
            modded = h.strip_digest(str(content))
            hashed = h.hashit(modded)
            writer("$$$$$$$$$$~~~~~~~~~~$$$$$$$$$$" + str(url) +
                   "$$$$$$$$$$~~~~~~~~~~$$$$$$$$$$".rstrip("\n").rstrip(" ")
                   + str(modded) +
                   "%%%%%%%%%%~~~~~~~~~~~%%%%%%%%%%" + str(url) +
                   "%%%%%%%%%%~~~~~~~~~~~%%%%%%%%%%".rstrip("\n").rstrip(" ")
                   ,"content")
            writer(url + "~" + str(hashed), "hashes")
            return True
        except Exception as e:
            print("Error!! in SkimUitls.manage_content " + str(e))
            self.lint("Error! in SkimUitls.manage_content " + str(e))

    def time_pretty(self, total_time: int):
        '''
        Take total time from perf timers and format nicely
        '''
        try:
            sec = int(total_time % 60)
            if sec < 10:
                sec = str(sec)
            minutes = total_time.__floordiv__(60)
            minutes = int(minutes)
            minutes = str(minutes)
            sec = str(sec)
            return minutes + ":" + sec
        except Exception as e:
            print("Error! in skim_utils.time_pretty: " + str(e))

    def test_internet(self):
        '''
        Test internet connectivity, proceed if successful.
        '''
        try:
            import requests
            google = requests.get("http://www.google.com", timeout=2)
            if (google.status_code == 200):
                return True
            else:
                return False
        except Exception as e:
            print("Error! in SkimUitls.test_internet: " + str(e))

    def clear_screen(self):
        '''
        Clear the terminal screen.
        '''
        try:
            import os
            os.system("clear")
        except Exception as e:
            print("Error! in clearscreen: " + str(e))

    def remove_orphan_files(self, path):
        '''
        Delete files left from failed executions
        '''
        try:
            import subprocess
            rm = subprocess.run(["rm -f " + str(path) + "*.txt"], stdout=subprocess.PIPE, shell=True)
            if rm.returncode != 0:
                raise Exception
            return True
        except Exception as e:
            print("Error!! in SkimUitls.remove_orphan_files: " + str(e))

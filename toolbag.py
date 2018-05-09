#!/usr/bin/env python3

import time

import datetime
import os
import random
import shlex
import subprocess
import systemd.daemon
import systemd.journal
import termcolor
from typing import List, Dict


class Toolbag:

    def __init__(self):
        self.colors: List = ['red', 'green', 'yellow', 'magenta', 'cyan']

    def clear_screen(self):
        try:
            os.system("clear")
        except Exception as e:
            print("Error! in toolbag.clearscreen: " + str(e))

    def lint(self, message: str, logname: str) -> bool:
        try:
            with open(str(logname), "a") as file:
                file.write(str(message) + "\n")
                file.close()
                print(str(message))
            return True
        except IOError as i:
            print("IO ERROR!!! in lint. logname is: " + str(logname) + "exception: " + str(i))
        except Exception as e:
            print("ERROR!!! in lint. logname is: " + str(logname) + "exception: " + str(e))

    def excepticon(self, method_name: str, exception: Exception):
        try:
            self.lint = ("Error!! in " + str(method_name) + " Error Message: " + str(exception))
        except Exception as e:
            print("Error! in Toolbag.excepticon() exception manager: " + str(e))

    def create_logfile(self, dir: str, application_name: str) -> str:
        try:
            current_time = self.create_timestamp()
            new_dir = str(dir)
            new_file_name = (str(application_name) + "-" + str(current_time))
            if not self.check_dir_exists(new_dir) or not self.check_file_exists(new_dir + new_file_name):
                raise IOError
            return (str(new_dir + new_file_name))
        except IOError as i:
            self.excepticon("IOERROR!!! in toolbag.create_logfile(): ", i)
        except Exception as e:
            self.excepticon("toolbag.create_logfile()", e)

    def create_timestamp(self) -> str:
        try:
            ts = datetime.datetime.now().strftime("%Y_%m_%d_%H_%M_%S")
            return str(ts)
        except Exception as e:
            self.excepticon("create_timestamp", e)

    def get_headers(self, browser) -> Dict:
        try:
            browser = str(browser)
            headers = {}
            if browser == "ie":
                headers = {
                    "User-Agent": "Mozilla/5.0 (compatible, MSIE 11, Windows NT 6.3; Trident/7.0;  "
                                         "rv:11.0) like Gecko",
                }
            if browser == "firefox":
                headers = {
                    "User-Agent": "Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:47.0) Gecko/20100101 Firefox/47.0",
                }
            if browser == "chrome":
                headers = {
                    "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) "
                                  "Chrome/51.0.2704.103 Safari/537.36",
                }
            return headers
        except Exception as e:
            print("Error! in toolbag.get_headers: " + str(e))
            self.excepticon("get_headers", e)

    def terminator(self, process: str) -> bool:
        try:
            pkil = subprocess.run([shlex.quote("/bin/pkill " + str(process))], shell=True)
            time.sleep(3)
            pkl = subprocess.run([shlex.quote("/bin/pkill -15 " + str(process))], shell=True)
            time.sleep(3)
            pkill = subprocess.run([shlex.quote("/bin/pkill -9 " + str(process))], shell=True)
            pkil_rc = pkil.returncode
            pkl_rc = pkl.returncode
            pkill_rc = pkill.returncode
            if (pkil_rc is 0) or (pkill_rc is 0) or (pkl_rc is 0):
                return True
            else:
                return False
        except Exception as e:
            self.excepticon("Terminator", e)


    def get_pids(self, name: str) -> List:
        '''
        Returns a list of PID numbers for a given name
        '''
        try:
            pids = []
            apd = pids.append
            pgrep = subprocess.run([shlex.quote("pgrep " + str(name))], stdout=subprocess.PIPE, shell=True)
            for pid in pgrep.stdout.splitlines():
                apd(pid.decode("utf-8"))
            return pids
        except Exception as e:
            print("Error!! in cleaner.get_pids(): " + str(e))


    def get_process_count(self, proc_name: str) -> int:
        try:
            cmd = shlex.quote("pgrep " + str(proc_name) + " | wc -l")
            pgrep = subprocess.run([cmd], stdout=subprocess.PIPE, shell=True)
            if pgrep.returncode != 0:
                raise Exception
            else:
                count = pgrep.stdout
                count = count.decode("utf-8")
                count = int(count)
                return count
        except Exception as e:
            self.excepticon("cleaner.get_number_pids()", e)

    def color(self, text: str, color: str) -> str:
        try:
            c = termcolor
            if color == "random":
                rand = random.randint(0, int(len(self.colors)-1))
                rnd_color = str(self.colors.__getitem__(int(rand)))
                return c.colored(str(text), str(rnd_color))
            else:
                return c.colored(str(text), str(color))
        except Exception as e:
            self.excepticon("color", e)

    def check_file_exists(self, filename: str):
        ''' If filename parameter does not exist, create it.
        '''
        try:
            file = str(filename)
            if (os.path.isfile(file)):
                return True
            else:
                tch = ("/bin/touch " + file)
                tch = shlex.quote(tch)
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
        '''If directory parameter does not exist, create it.
        '''
        try:
            if (os.path.isdir(str(dir))):
                return True
            else:
                cmd = ("/bin/mkdir " + str(dir))
                cmd = shlex.quote(cmd)
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

    def build_allports_list(self) -> List:
        try:
            new_port_list = []
            i = int(0)
            max = int(65536)
            apd = new_port_list.append
            while i < max:
                apd(i)
                i += 1
            random.shuffle(new_port_list)
            return new_port_list
        except Exception as e:
            print("Error! in atlas.build_allports_list: " + str(e))

    def get_port_list(self):
        try:
            ports = [
            7, 11, 13, 15, 17, 19, 21, 22, 23, 25, 26, 37, 49, 53, 69, 70, 79, 80, 81, 82, 83, 84, 88, 102, 104,
            110, 111, 113, 119, 123, 129, 137, 143, 161, 175, 179, 195, 311, 389, 443, 444, 445, 465, 500, 502,
            503, 515, 520, 523, 554, 587, 623, 626, 631, 636, 666, 771, 789, 873, 902, 992, 993, 995, 1010, 1023,
            1025, 1099, 1177, 1200, 1234, 1311, 1400, 1434, 1471, 1515, 1521, 1599, 1604, 1723, 1741, 1770, 1777,
            1883, 1900, 1911, 1962, 1991, 2000, 2067, 2081, 2082, 2083, 2086, 2087, 2123, 2152, 2181, 2222, 2323,
            2332, 2375, 2376, 2379, 2404, 2455, 2480, 2628, 3000, 3001, 3128, 3260, 3283, 3299, 3306, 3310, 3386,
            3388, 3389, 3460, 3541, 3542, 3689, 3702, 3749, 3780, 3784, 3790, 4000, 4022, 4343, 4040, 4063, 4064,
            4070, 4369, 4434, 4443, 4444, 4500, 4567, 4664, 4730, 4782, 4786, 4800, 4840, 4848, 4911, 4949, 5000,
            5001, 5006, 5007, 5008, 5009, 5060, 5094, 5222, 5269, 5353, 5357, 5432, 5555, 5560, 5577, 5601, 5632,
            5672, 5683, 5800, 5801, 5858, 5900, 5901, 5938, 5984, 5985, 5986, 6000, 6001, 6379, 6664, 6666, 6667,
            6881, 6969, 7071, 7218, 7474, 7547, 7548, 7634, 7657, 7777, 7779, 8000, 8001, 8008, 8009, 8010, 8060,
            8069, 8080, 8081, 8086, 8087, 8089, 8090, 8098, 8099, 8112, 8126, 8139, 8140, 8181, 8333, 8334, 8443,
            8554, 8649, 8800, 8834, 8880, 8888, 8889, 9000, 9001, 9002, 9009, 9042, 9051, 9080, 9100, 9151, 9160,
            9191, 9200, 9306, 9418, 9443, 9595, 9600, 9869, 9943, 9944, 9981, 9999, 10000, 10001, 10243, 10443,
            10554, 11211, 11300, 11443, 12000, 12345, 13579, 14147, 16010, 16992, 16993, 17000, 18081, 18245, 20000,
            20547, 21025, 21379, 23023, 23424, 25105, 25565, 27015, 27016, 27017, 28015, 28017, 30718, 32400, 32764,
            37777, 41794, 44818, 47808, 48899, 49152, 49153, 49494, 50070, 50100, 51106, 53413, 54138, 55443, 55553,
            55554, 62078, 64738
        ]
            random.shuffle(ports)
            return ports
        except Exception as e:
            self.excepticon("get_port_list", e)

    def shuffler(self, array: List) -> List:
        try:
            random.shuffle(array)
            return array
        except Exception as e:
            print("Error! in toolbag.shuffler(): " + str(e))

    def sd_notify(self, message: str):
        try:
            if message == "watchdog":
                systemd.daemon.notify(systemd.daemon.Notification.WATCHDOG)
                systemd.journal.write("watchdog = 1 sent.")
                time.sleep(1)
            if message == "ready":
                systemd.daemon.notify(systemd.daemon.Notification.READY)
                systemd.journal.write("ready = 1 sent.")
                time.sleep(2)
        except Exception as e:
            print("Error in toolbag.sd_notify " + str(e))

    def perf(self):
        try:
            return time.perf_counter()
        except Exception as e:
            print("Error! in toolbag.perf: " + str(e))





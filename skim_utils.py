#!/usr/bin/env python3


class SkimUitls:

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

    def get_port_list(self):
        try:
            import random
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
            print("Error! get_port_list", e)


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
            writer("\n\n$$$$$$$$$$~~~~~~~~~~$$$$$$$$$$" + str(url) + "$$$$$$$$$$~~~~~~~~~~$$$$$$$$$$\n"
                   + str(modded) +
                   "\n%%%%%%%%%%~~~~~~~~~~~%%%%%%%%%%" + str(url) + "%%%%%%%%%%~~~~~~~~~~~%%%%%%%%%%"
                   ,"content")
            writer(url + "~" + str(hashed), "hashes")
            return True
        except Exception as e:
            print("Error!! in SkimUitls.manage_content " + str(e))
            self.lint("Error! in SkimUitls.manage_content " + str(e))

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

#!/usr/bin/env python3

import requests
import skim_controller
import skim_hasher
import skim_writer_io
import subprocess
import toolbag


class SkimUitls:

    def lint(self, message: str) -> bool:
        '''
        Log and print at the same time.
        '''
        try:
            message = str(message)
            ts = toolbag.Toolbag().create_timestamp()
            ts = str(ts)
            logfile = skim_controller.SkimController().logfile
            with open(logfile, "a") as file:
                file.write(ts + " : - " + message + "\n")
                file.close()
                print(message)
            return True
        except IOError as i:
            print("IO Error in SkimUitls.lint: " + str(i))
        except Exception as e:
            print("Error in SkimUitls.lint" + str(e))

    def manage_content(self, url: str, content: str) -> bool:
        '''
        Take content from HTTP response, remove dynamic elements,
        store content and hash for comparison on next pass
        '''
        try:
            writer = skim_writer_io.Skim_writer_io().writer
            h = skim_hasher.Hasher()
            modded = h.strip_digest(str(content))
            hashed = h.hashit(modded)
            writer("\n\n$$$$$$$$$$~~~~~~~~~~~~~$$$$$$$$$$\n" + str(url)
                   + "\n$$$$$$$$$$~~~~~~~~~~~~~$$$$$$$$$$\n" + str(modded)
                   + "\n%%%%%%%%%%%%~~~~~~~~~~~~~~~~~~~~%%%%%%%%%%%%\n\n",
                        "content")
            writer(url + "~" + str(hashed), "hashes")
            return True
        except Exception as e:
            print("Error!! in SkimUitls.manage_content " + str(e))
            self.lint("Error! in SkimUitls.manage_content " + str(e))

    def test_internet(self):
        '''
        Test internet connectivity, proceed if successful
        '''
        google = requests.get("http://www.google.com", timeout=2)
        if (google.status_code == 200):
            return True
        else:
            return False

    def remove_orphan_files(self, path):
        '''
        Delete files left from failed executions
        '''
        try:
            rm = subprocess.run(["rm -f " + str(path) + "*.txt"], stdout=subprocess.PIPE, shell=True)
            if rm.returncode != 0:
                raise Exception
            return True
        except Exception as e:
            print("Error!! in SkimUitls.remove_orphan_files: " + str(e))

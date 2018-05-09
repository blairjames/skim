#!/usr/bin/env python3

import toolbag


class Skim_writer_io:
    '''
    Handle FileIO writes, writing to files according to parameters.
    '''
    def writer(self, site: str, file_name: str) -> bool:
        try:
            ts = toolbag.Toolbag().create_timestamp()
            base_path: str = "/root/scripts/skim/output/"
            with open(str(base_path) + str(file_name) + ".txt", "a") as file:
                file.write(str(ts) + ": " + str(site) + "\n")
                file.close()
            return True
        except Exception as e:
            print("Error! in Skim_writer_io.writer: " + str(e))



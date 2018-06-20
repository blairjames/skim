#!/usr/bin/env python3

from time import perf_counter
from typing import List
import skim_content_check


class SkimNotResponding:
    '''
    Read list of non-responding sites and re-test.
    Test HTTPS
    '''

    def __init__(self):
        self.perf_read_file: str = ""
        self.perf_clean_list: str = ""

    def read_file(self, filename: str) -> List:
        p1 = perf_counter()
        non_res_urls = []
        apnd = non_res_urls.append
        with open(str(filename), "r") as file:
            [apnd(f) for f in file.readlines()]
        p2 = perf_counter()
        self.perf_read_file = str(round(p2 - p1, 6))
        return non_res_urls

    def clean_list(self, the_list: List) -> List:
        p1 = perf_counter()
        new_list = []
        apnd = new_list.append
        [apnd(el) for el in the_list]
        p2 = perf_counter()
        self.perf_clean_list = str(round(p2 - p1, 6))
        return new_list


def main():
    new_skim_not_res = SkimNotResponding()
    check = skim_content_check.SkimContentCheck()
    dirname = skim_content_check.SkimContentCheck().get_dir_name_cmd_builder("most_recent")
    print("!!!   Not Responding dirname: - " + str(dirname))

    #TODO: cmd is wrong in contect  check print
    most_recent_dir = check.get_dir_name("ls " + dirname + "/*not_res*")

    print("most recent: " + str(most_recent_dir))
    file_off_disk = new_skim_not_res.read_file(most_recent_dir)

    print("file off: " + str(file_off_disk))
    clean_list = new_skim_not_res.clean_list(file_off_disk)

    print(new_skim_not_res.perf_read_file)
    print(new_skim_not_res.perf_clean_list)
    x = [print(x) for x in clean_list]


if __name__ == '__main__':
    main()
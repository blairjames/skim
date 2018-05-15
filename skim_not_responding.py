#!/usr/bin/env python3

from time import perf_counter
import skim_requester


class SkimNotResponding:
    '''
    Read list of non-responding sites and re-test.
    Test HTTPS
    '''

    def __init__(self):
        self.perf_read_file: str = ""
        self.perf_clean_list: str = ""

    def read_file(self):
        p1 = perf_counter()
        non_res_urls = []
        apnd = non_res_urls.append
        filename = "/root/scripts/skim/output/2018_05_14_21_32_45/not_responding.txt"
        with open(filename, "r") as file:
            for f in file.readlines():
                apnd(f)
        p2 = perf_counter()
        self.perf_read_file = p2 - p1
        return non_res_urls

    def clean_list(self, the_list):
        p1 = perf_counter()
        new_list = []
        apnd = new_list.append
        for el in the_list:
            el = str(el)
            el = el.rstrip("\n").rstrip(" ")
            apnd(el)
        p2 = perf_counter()
        self.perf_clean_list = p2 - p1
        return new_list












def main():
    new_skim_not_res = SkimNotResponding()
    file_off_disk = new_skim_not_res.read_file()
    clean_list = new_skim_not_res.clean_list(file_off_disk)
    print(new_skim_not_res.perf_read_file)
    print(new_skim_not_res.perf_clean_list)
    for x in clean_list:
        print(x)

if __name__ == '__main__':
    main()
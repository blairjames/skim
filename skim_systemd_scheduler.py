#!/usr/bin/env python3

import time

import skim_content_check
import skim_controller
from skim_utils import SkimUitls as utl


def main():
    '''
    Scheduler sits in memory, monitored by systemd
    '''
    try:
        sleep_time: int = 300
        skim_controller.main()
        print("&*&*&**&*&*&*&*&^^^^^^^^^^ scheduler loop after main before display results")
        time.sleep(3)
        skim_controller.SkimController().display_results()
        skim_content_check.main()
        utl().lint(("\nNow sleeping for " + str(sleep_time) + " seconds.\n"))
        time.sleep(sleep_time)
    except Exception as e:
        print("Error! in Skim_systemd.main(): ", str(e))
        exit(1)

if __name__ == '__main__':
    main()

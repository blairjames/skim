#!/usr/bin/env python3

import time

import skim_content_check
import skim_controller


def main():
    '''
    Scheduler sits in memory, monitored by systemd
    '''
    try:
        sleep_time: int = 300
        go_to_sleep = time.sleep
        while True:
            if not skim_controller.main():
                raise Exception
            if not skim_content_check.main():
                raise Exception
            from skim_utils import SkimUitls as utl
            utl().lint(("\nNow sleeping for " + str(sleep_time) + " seconds.\n"))
            go_to_sleep(sleep_time)

    except Exception as e:
        print("Error! in Skim_systemd.main(): ", str(e))

if __name__ == '__main__':
    main()

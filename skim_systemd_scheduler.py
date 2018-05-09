#!/usr/bin/env python3

import time

import skim_content_check
import skim_controller


def main():
    '''
    Schedular sits in memory, watched by systemd
    '''
    try:
        while True:
            if not skim_controller.main():
                raise Exception
            if not skim_content_check.main():
                raise Exception
            time.sleep(300)
    except Exception as e:
        print("Error! in Skim_systemd.main(): ", str(e))

if __name__ == '__main__':
    main()

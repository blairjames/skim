#!/usr/bin/env python3


def main():
    '''
    Scheduler sits in memory, monitored by systemd
    '''
    try:
        from time import sleep
        import skim_content_check
        import skim_controller
        from skim_utils import SkimUitls as utl
        while True:
            sleep_time: int = 600
            skim_controller.main()
            skim_content_check.main()
            utl().lint(("\nNow sleeping for " + str(sleep_time) + " seconds.\n"))
            sleep(sleep_time)

    except Exception as e:
        print("Error! in Skim_systemd.main(): ", str(e))
        exit(1)

if __name__ == '__main__':
    main()

#!/usr/bin/env python3


def main():
    '''
    Scheduler sits in memory, monitored by systemd.
    Handles order of execution and waiting in between passes.
    '''
    try:
        from time import sleep
        import skim_content_check
        import skim_controller
        from skim_utils import SkimUitls as utl
        ctrl = skim_controller
        while True:
            sleep_time: int = 120
            ctrl.main()
            skim_content_check.main()
            ctrl.SkimController().display_results()
            utl().lint(("\nNow sleeping for " + str(sleep_time) + " seconds.\n"))
            sleep(sleep_time)

    except Exception as e:
        print("Error! in Skim_systemd.main(): ", str(e))
        exit(1)

if __name__ == '__main__':
    main()

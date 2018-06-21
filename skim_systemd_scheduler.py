#!/usr/bin/env python3


def main():
    '''
    Scheduler sits in memory, monitored by systemd.
    Handles order of execution and waiting in between passes.
    '''
    try:
        from time import sleep, perf_counter
        import skim_content_check
        import skim_controller
        from skim_utils import SkimUitls as utl
        ctrl = skim_controller
        while True:
            p1 = perf_counter()
            sleep_time: int = 600
            ctrl.main()
            skim_content_check.main()
            p2 = perf_counter()
            total_time = p2 - p1
            time = utl().time_pretty(total_time)
            lnt = utl().lint
            lnt("\nExecution time: " + str(time) + "\n")
            lnt("\nNow sleeping for " + str(sleep_time) + " seconds.\n")
            ctrl.SkimController().display_results()
            sleep(sleep_time)

    except Exception as e:
        print("Error! in Skim_systemd.main(): ", str(e))
        exit(1)

if __name__ == '__main__':
    main()

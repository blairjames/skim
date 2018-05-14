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
            print("^^^^^into While True\n")
            p1 = perf_counter()
            print("^^^^^number 1\n")
            sleep_time: int = 30
            print("^^^^^number 2\n")
            ctrl.main()
            print("^^^^^number 3\n")
            skim_content_check.main()
            print("^^^^^number 4\n")
            p2 = perf_counter()
            print("^^^^^number 5\n")
            total_time = p2 - p1
            print("^^^^^number 6 " + str(total_time))
            time = utl().time_pretty(total_time)
            print("^^^^^number 7 " + str(time))
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

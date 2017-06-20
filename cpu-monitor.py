from datetime import datetime
import sys
import time


def moving_average(average, new_sample, n):
    average -= average / float(n)
    average += new_sample / float(n)

    return average


def main_function():
    if len(sys.argv) != 4:
        print "Usage: cpu-monitor path-to-proc-stats interval-whole-seconds window"
        quit()

    proc_stats_path = sys.argv[1]
    monitor_interval = int(sys.argv[2])
    n = int(sys.argv[3])

    total_jiffies_1 = None
    work_jiffies_1 = None
    average = 0.0

    while True:
        with(open(proc_stats_path, "r")) as stats:
            cpu_data = stats.readline()
            cpu_parts = map(int, cpu_data.split()[1:-1])
            total_jiffies_2 = sum(cpu_parts)
            work_jiffies_2 = sum(cpu_parts[0:3])

            epoch = datetime.now().strftime('%Y-%m-%dT%H:%M:%S')

            if total_jiffies_1 is not None and work_jiffies_1 is not None:
                work_over_period = work_jiffies_2 - work_jiffies_1
                total_over_period = total_jiffies_2 - total_jiffies_1
                if total_over_period != 0:
                    percent_cpu = float(work_over_period) / float(total_over_period) * 100
                else:
                    percent_cpu = 0.0
                new_average = moving_average(average, percent_cpu, n)
                print epoch, new_average
                average = new_average

            # print cpu_parts
            # print total_jiffies_2
            # print work_jiffies_2

            total_jiffies_1 = total_jiffies_2
            work_jiffies_1 = work_jiffies_2

        time.sleep(monitor_interval)

if __name__ == '__main__':
    main_function()
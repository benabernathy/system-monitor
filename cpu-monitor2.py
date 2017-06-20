from datetime import datetime
import re
import socket
import sys
import time


def main_function():
    if len(sys.argv) != 4:
        print "Usage: cpu-monitor path-to-proc-stats output-file interval-whole-seconds"
        quit()

    proc_stats_path = sys.argv[1]
    output_file_path = sys.argv[2]
    monitor_interval = int(sys.argv[3])

    machine_name = socket.gethostname()

    with(open(output_file_path, 'a')) as output:
        while True:
            with(open(proc_stats_path, 'r')) as stats:

                epoch = datetime.now().strftime('%Y-%m-%dT%H:%M:%S')

                for cpu_data in stats:
                    cpu_name = cpu_data.split()[0]
                    if "cpu" in cpu_name:
                        output.write(machine_name + ',' + epoch + ',' + re.sub('\s+', ',', cpu_data.strip()) + '\n')
                    else:
                        break
                output.flush()
            time.sleep(monitor_interval)

if __name__ == '__main__':
    main_function()
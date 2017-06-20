from datetime import datetime
import re
import socket
import sys
import time


def main_function():
    if len(sys.argv) != 4:
        print "Usage: mem-monitor path-to-meminfo output-file interval-whole-seconds"
        quit()

    meminfo_path = sys.argv[1]
    output_file_path = sys.argv[2]
    monitor_interval = int(sys.argv[3])

    machine_name = socket.gethostname()

    total_memory_re = re.compile(r'MemTotal:\s+\d+')
    memory_free_re = re.compile(r'MemFree:\s+\d+')
    buffers_re = re.compile(r'Buffers:\s+\d+')
    cached_re = re.compile(r'Cached:\s+\d+')
    swap_total_re = re.compile(r'SwapTotal:\s+\d+')
    swap_free_re = re.compile(r'SwapFree:\s+\d+')

    with(open(output_file_path, 'a')) as output:
        output.write('machine_name,epoch,total_memory,free_memory,buffers,cached,total_swap,free_swap\n')
        while True:
            with(open(meminfo_path, "r")) as stats:
                epoch = datetime.now().strftime('%Y-%m-%dT%H:%M:%S')
                mem_stats = stats.read()

                total_mem = total_memory_re.findall(mem_stats)[0].strip().split(' ')[-1]
                memory_free = memory_free_re.findall(mem_stats)[0].strip().split(' ')[-1]
                buffers = buffers_re.findall(mem_stats)[0].strip().split(' ')[-1]
                cached = cached_re.findall(mem_stats)[0].strip().split(' ')[-1]
                swap_total = swap_total_re.findall(mem_stats)[0].strip().split(' ')[-1]
                swap_free = swap_free_re.findall(mem_stats)[0].strip().split(' ')[-1]

                output.write(machine_name + ',' + epoch + ',' + total_mem + ',' + memory_free + ',' + buffers + ',' \
                      + cached + ',' + swap_total + ',' + swap_free + '\n')

                output.flush()
            time.sleep(monitor_interval)


if __name__ == '__main__':
    main_function()

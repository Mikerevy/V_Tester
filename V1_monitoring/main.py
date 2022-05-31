# Importing the library for getting cpu, memory ..
import psutil
import pandas as pd
import time


def main():
    try:
        user_pid = int(input("Insert PID process: "))
        user_iteration = int(input("How many iterations: "))
        user_time_interval = float(input("Interval for collect data: "))
        # Call ftion to get lists of values we want
        cpu_usage, time_list, working_set_memory, private_bytes_memory, handles = get_an_info(user_pid, user_iteration,
                                                                                              user_time_interval)
    # In case user provided bad input, there are set default values.
    except ValueError:
        print("Something went wrong.")
        print("Default values are: PID=None, iteration= 10, time interval = 1second")
        cpu_usage, time_list, working_set_memory, private_bytes_memory, handles = get_an_info()

    # Call ftion that convert our lists of values to the .csv
    convert_to_csv(cpu_usage, time_list, working_set_memory, private_bytes_memory, handles)


# Ftion for getting inf about CPU, memory and handles
def get_an_info(pid=None, iteration=10, interval=1):
    # Create object process
    process = psutil.Process(pid)

    # Initialize empty lists and variables
    time_list, cpu_usage, working_set_memory, private_bytes_memory, handles = ([] for i in range(5))

    for _ in range(iteration):
        # Get CPU usage with specific time interval
        cpu_usage.append(process.cpu_percent(interval))  # if CPU% > 100% -> the process running multiple threads

        # Get current time and format to the str
        t = time.localtime()
        current_time = time.strftime("%H:%M:%S", t)
        time_list.append(current_time)

        # Get Working set memory (Resident set for Linux)
        working_set_memory.append(round(process.memory_info().rss / 1024 / 1024, 2))

        # Get Private Bytes (Virtual Memory Sizeking set)
        private_bytes_memory.append(round(process.memory_info().vms / 1024 / 1024, 2))

        # Get Number of handles
        handles.append(process.num_handles())

    return cpu_usage, time_list, working_set_memory, private_bytes_memory, handles


# Convert our lists of values to the .csv
def convert_to_csv(cpu, timee, work_mem, priv_mem, hand):
    dict = {"Time": timee, "CPU": cpu,
            "Working set": work_mem, "Private Bytes": priv_mem,
            "Open handles": hand}

    # Create a Dataframe
    df = pd.DataFrame(dict)
    # Convert to .csv
    df.to_csv('info.csv', index=False)


# Call main ftion
main()

"""
I am able to prompt user to insert path of .exe file
        * Then open the file
        * Then get a PID
        - if I use this PID to my Process() class ->  process = psutil.Process(pid)
        - It returns me PID number, I use it to my function to find out the cpu...
            the error is: 'psutil.NoSuchProcess: process no longer exists.'...
            (I tried to google it, but there are not to many info about it)

**** The Code for run calc and find out PID could looks like this ****
    import subprocess
    open_calc = subprocess.Popen('C:\\Windows\\System32\\calc.exe')
    pid = open_calc.pid
    print(pid)
    process = psutil.Process(pid)
    process.cpu_percent(1) -> 'psutil.NoSuchProcess: process no longer exists.'
"""

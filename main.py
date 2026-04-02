#v1
import re #regular expressions, which help extract specific patterns from text
from collections import deque # A double-ended queue
max_idle_iterations = 100
idle_iterations = 0

def read_input_file(filename):
    processes = []
    with open(filename, 'r') as file:
        for line in file:
            parts = line.split()
            pid = int(parts[0])
            arrival_time = int(parts[1])
            priority = int(parts[2])
            bursts = []
            remaining_line = " ".join(parts[3:])
            pattern = r"(CPU\{(.*?)\}|IO\{(.*?)\})"
            matches = re.findall(pattern, remaining_line)
            for match in matches:
                if match[0].startswith('CPU'):
                    cpu_details = parse_cpu_burst(match[1])
                    bursts.append(('CPU', cpu_details))
                elif match[0].startswith('IO'):
                    io_details = parse_io_burst(match[2])
                    bursts.append(('IO', io_details))
            processes.append({
                'PID': pid,
                'Arrival Time': arrival_time,
                'Priority': priority,
                'Bursts': bursts
            })
    return processes

def parse_cpu_burst(burst_string): #Extracts CPU burst details, which may include execution time, resource requests, or releases.
    actions = []
    components = burst_string.split(',')
    for component in components:
        component = component.strip()
        if component.startswith('R'):
            resource = re.search(r'R\[(\d+)\]', component)
            if resource:
                actions.append(('Request', int(resource.group(1))))
        elif component.startswith('F'):
            resource = re.search(r'F\[(\d+)\]', component)
            if resource:
                actions.append(('Release', int(resource.group(1))))
        else:
            actions.append(('Time', int(component)))
    return actions

def parse_io_burst(burst_string):
    time = int(burst_string.strip())
    return [('Time', time)]



resource_ids = [1, 2, 3,6,7,8,9,10,11,12,13,14,15]  # Resource IDs: R1, R2, R3
# Define a dictionary to track the availability of resources
resource_flags = {resource_id: 1 for resource_id in resource_ids}

def detect_deadlock(resource_holdings, resource_waiting_queue, resource_id_waite):
    #print("****************************************************************************")
    #print("****************************************************************************")
    #print("resource_holdings",resource_holdings,"resource_waiting_queue" ,resource_waiting_queue,"resource_id_waite", resource_id_waite)
    #print("****************************************************************************")
    #print("****************************************************************************")
    waiting_on = {}
    for process, _ in resource_waiting_queue:
        pid = process['PID']
        resource_id = resource_id_waite.get(pid)
        waiting_on[pid] = resource_id

    visited = set()

    def has_cycle(process):
        if process in visited:
            return True
        visited.add(process)
        resource = waiting_on.get(process)
        if resource is None:
            return False
        holder = resource_holdings.get(resource)
        if holder is None or holder not in waiting_on:
            return False
        return has_cycle(holder)

    for pid in waiting_on:
        visited.clear()
        if has_cycle(pid):
            return True

    return False

def recover_deadlock(resource_holdings, resource_waiting_queue, ready_queue, resource_flags):

    #print("****************************************************************************")
    #print("****************************************************************************")
    #print("resource_holdings",resource_holdings,"resource_waiting_queue" ,resource_waiting_queue,"ready_queue", ready_queue,"resource_flags", resource_flags)
    #print("****************************************************************************")
    #print("****************************************************************************")

    if resource_waiting_queue:
        deadlock_process = resource_waiting_queue.popleft()
      #  print(deadlock_process)
        pid = deadlock_process[0]['PID']

        for resource_id, holder_pid in list(resource_holdings.items()):
            if holder_pid == pid:
                resource_holdings[resource_id] = None
                resource_flags[resource_id] = 1

       # print("resource_holdings", resource_holdings, "resource_waiting_queue", resource_waiting_queue, "ready_queue",ready_queue, "resource_flags", resource_flags)
        newwww, _ = resource_waiting_queue.popleft()
        #print("newwww", newwww)
        ready_queue.append(newwww)
        resource_waiting_queue.append(deadlock_process)
        print(f"Deadlock detected. Process {pid} terminated for recovery.")

        return pid

    return None

def simulate_scheduling(processes, quantum):
    gantt_chart = []
    ready_queue = deque()
    waiting_queue = deque()
    resource_waiting_queue = deque()
    time = 0
    completed_processes = []
    process_waiting_times = {}  # Dictionary to store waiting times for each process
    r=0
    tt=0
    resource_holdings = {resource_id: None for resource_id in resource_ids}  # Map each resource to the process that holds it
    resource_id_waite={}
    hemo=0
    new=1
    new1=1

    while processes or ready_queue or waiting_queue or resource_waiting_queue:
        previous_time = time
        # Add arriving processes to the ready queue
        i=0
        while i < len(processes) :
           while processes and processes[i]['Arrival Time'] <= time :
               #l1= time - processes[0]['Arrival Time']
               process = processes.pop(i)
               if(i != 0 and i != len(processes) - 1):
                  i=i-1
               ready_queue.append(process)
               # process_waiting_times[process['PID']] = -(l1)   # Initialize waiting time for new processes
               process_waiting_times[process['PID']] = 0
           i=i+1

        # Process execution
        if ready_queue:
            ready_queue = deque(sorted(ready_queue, key=lambda x: x['Priority']))  # Sort by priority
            current_process = ready_queue.popleft()  # Get the process with highest priority
            burst = current_process['Bursts'][0]
            #print(current_process['Bursts'][0])
            if burst[0] == 'CPU':
                #print("ppppppp",burst[0] ,burst[1])
                cpu_time = 0
                new_actions = []
                resources_to_release = []  # Track resources to release after the burst

                for action in burst[1]:
                   # print ("time ",time)
                    if action[0] == 'Time':
                        cpu_time += action[1]
                        #print("p",current_process['PID'],"cpu_time",cpu_time,action[1])
                        #print("3333333333333333---",burst[1][burst[1].index(action) + 1:])
                        if current_process['Bursts'][0][1][0][1] == 0 :
                            burst11=('CPU',burst[1][burst[1].index(action) + 1:])
                            current_process['Bursts'][0] = burst11
                        if action[1] >= quantum:
                            # If the CPU time exceeds the quantum, we need to split the burst and store the remaining part
                            remaining_actions = [('Time', cpu_time - quantum)] + burst[1][burst[1].index(action) + 1:]
                            # Save the remaining CPU burst after executing for the quantum time
                            new_burst = ('CPU', remaining_actions)
                           # print("befor",current_process['Bursts'][0])
                            current_process['Bursts'][0] = new_burst
                           # print("new_burst",new_burst)
                            # Add this process back to the ready queue to resume later
                           # print("readyyyyyyyyyyyyyyyyyyyyyyyy-->",ready_queue)
                            #ready_queue.append(current_process)
                            new=0
                            # Break here to ensure we don't process further actions in this burst
                            break
                        if (burst[1][burst[1].index(action) + 1:] == []):
                            #print(current_process['Bursts'][0])
                            new_burst=('CPU', burst[1][burst[1].index(action) + 1:])
                            current_process['Bursts'][0] = new_burst
                            #print(current_process['Bursts'])
                            new = 0
                    elif action[0] == 'Request':
                        resource_id = action[1]  # Extract resource ID from the action
                       # print("resource_id", resource_id,"resource_flags", resource_flags[resource_id])
                        # Check if the resource is available and not reserved by the current process
                        if resource_flags[resource_id] == 0 and resource_holdings[resource_id] != current_process[
                            'PID']:
                           # print("unavilaple p ",current_process['PID'],"r",resource_id)
                            resource_id_waite[current_process['PID']]=resource_id
                        #    print("resource_id_waite", resource_id_waite)
                            # Resource is not available or is reserved by another process, so put process in waiting queue
                            if cpu_time > 0:
                                # Save the current burst details (remaining CPU time and future resource requests)
                                #saved_burst = []  # To save remaining burst details, such as CPU{R[1], 10, F[2], F[1]}
                                remaining_action11 = ([('Request', resource_id)] + burst[1][burst[1].index(action) + 1:])  # Assuming burst[1] contains the resource requests
                                #    saved_burst.append(remaining_action11)  # Save the remaining actions for later
                                new_burstrr = ('CPU', remaining_action11)
                                current_process['Bursts'][0] = new_burstrr
                                new1=0
                               # print("Saving remaining burst details for later:", current_process)

                                # Now break, as we need to process the saved burst after resources are available
                                break
                            if cpu_time == 0:
                               process_waiting_times[current_process['PID']] += hemo
                               hemo=0
                               resource_waiting_queue.append((current_process, time + cpu_time))
                              # print("we put it in wait resource queue", resource_waiting_queue)
                               tt = 1
                            break
                        else:
                           if resource_flags[resource_id] == 1 and resource_holdings[resource_id] != current_process[
                                 'PID'] and cpu_time-quantum <= 0:
                                # Resource is available, reserve it
                              #  print("p",current_process['PID'] ,"enter here r " ,resource_id)
                                resource_flags[resource_id] = 0
                                resource_holdings[resource_id] = current_process['PID']  # Link the resource to the process
                                new_actions.append(action)
                                # Move to the next request only after the current one is fully completed
                                #ffflag=1
                                # break  # This ensures we don't proceed to the next resource request before completing the current one


                    elif action[0] == 'Release':
                       # print("release enter")
                        resource_id = action[1]
                        resources_to_release.append(resource_id)
                        #print("bbbbb",burst[1][burst[1].index(action) + 1][0])
                        burst22 = ('CPU', burst[1][burst[1].index(action) + 1:])
                        current_process['Bursts'][0] = burst22
                        new_actions.append(action)
                       # new=0
                      #  break


                if (tt):
                    tt=0
                    Deadlock = detect_deadlock(resource_holdings, resource_waiting_queue, resource_id_waite)
                   # print("Deadlock", Deadlock)
                    # Deadlock detection
                    if Deadlock:
                        print("\nwe enter deadlock at time",time)
                        recover_deadlock(resource_holdings, resource_waiting_queue, ready_queue, resource_flags)
                        continue
                    continue

                execute_time = min(cpu_time, quantum)
                f=execute_time
                r += f
                #print("time",time,"r",r)
                # Add arriving processes to the ready queue
                j = 0
                while j < len(processes):
                    while processes and processes[j]['Arrival Time'] <= r:
                        l= time - processes[j]['Arrival Time']
                        #print("l",l)
                        if (processes[j]['Arrival Time'] % quantum != 0):
                            hemo = l
                        process = processes.pop(j)
                        if (j != 0 and j != len(processes) - 1):
                           j=j-1
                        ready_queue.append(process)
                        process_waiting_times[process['PID']] = l  # Initialize waiting time for new processes
                    j=j+1

                #print(time)
                #if waiting_queue:
                 #  print(waiting_queue[0][1] )
                if waiting_queue and waiting_queue[0][1] <= (time+execute_time):
                 #   print("enterrrrrrrrrrrrrrrrrrrrrrrrrrrr")
                 #   print("***********************",time - waiting_queue[0][1])
                 #   print("PID:",waiting_queue[0][0]['PID'])
                    process_waiting_times[waiting_queue[0][0]['PID']] += (time - waiting_queue[0][1])
                    ready_queue.append(waiting_queue.popleft()[0])

                # Increment waiting time for all processes currently in the ready queue
                for process in ready_queue:
                  #  print(process['PID'])
                    process_waiting_times[process['PID']] += f  # Increment waiting time

               # print("#####################")
               #  Print the updated waiting times for all processes in the ready queue
               # print("Ready Queue Status:")
               # for process in ready_queue:
               #     print(f"Process {process['PID']} - Waiting Time: {process_waiting_times[process['PID']]}")
                if time != time + execute_time :
                    gg=time + execute_time
                    if time > time + execute_time:
                        gg+=quantum
                    gantt_chart.append((current_process['PID'], time, gg))
                    if time > time + execute_time:
                       time += quantum
                time += execute_time
                pp=0
                if cpu_time > execute_time:
                    remaining_time = cpu_time - execute_time
                    new_actions = [('Time', remaining_time)] + new_actions
                    burst = ('CPU', new_actions)
                    if(new):
                       current_process['Bursts'][0] = burst
                    #print("#############")
                    #print("checkkkk",current_process)
                    #print("#############")
                    ready_queue.append(current_process)
                    #else:
                     #  new=1
                     #  ready_queue.append(new_burst)
                else:
                    #print("enterrrrrrrrrrrrrrrrrr")
                    pp=1
                    if new1:
                       current_process['Bursts'].pop(0)
                    #print(current_process['Bursts'])
                    if current_process['Bursts']:
                        if current_process['Bursts'][0][0] == 'IO':
                            waiting_queue.append((current_process, time + current_process['Bursts'][0][1][0][1]))
                            current_process['Bursts'].pop(0)
                        else:
                           # print("HMMMMMMMMMMMMMMM")
                            #print(current_process['Bursts'][0][1] != [])
                            #if (current_process['Bursts']):
                            if current_process['Bursts'][0][1] != []:
                              # print(current_process['Bursts'])
                               ready_queue.append(current_process)
                            else:
                              #print(len(current_process['Bursts'][0:]))
                              if len(current_process['Bursts'][0:]) == 1 :
                                completed_processes.append(current_process)
                              else:
                                  #print(current_process['Bursts'][1:] ,current_process['Bursts'])
                                  current_process['Bursts'] = current_process['Bursts'][1:]
                                  #print(current_process['Bursts'])
                                  if current_process['Bursts'][0][0] == 'IO':
                                      waiting_queue.append(
                                          (current_process, time + current_process['Bursts'][0][1][0][1]))
                                      current_process['Bursts'].pop(0)

                    else:
                       # print("HMMMMMMMMMMMMMMMMMMMMMMMMMMM11111")
                        completed_processes.append(current_process)

            for resource_id in resources_to_release:
              if pp:
               # print(resources_to_release)
               # print("enterr hereeeeeee")
                resource_flags[resource_id] = 1
               # print("we free r", resource_id)
                temp_queue = deque()
               # print(resource_waiting_queue,resource_id)
                while resource_waiting_queue:
                    waiting_process,_= resource_waiting_queue.popleft()
                    waiting_resource_id = resource_id_waite[waiting_process['PID']]
                   # print("enterr hereeeeeee1111111111111111111111")
                   # print("waiting_process",waiting_process,"waiting_resource_id" ,waiting_resource_id,resource_id)
                    if waiting_resource_id == resource_id:
                        ready_queue.append(waiting_process)
                    else:
                        temp_queue.append((waiting_process, waiting_resource_id))
                    if not  resources_to_release:
                        break
                resource_waiting_queue = temp_queue

        if waiting_queue and waiting_queue[0][1] <= time:
            ready_queue.append(waiting_queue.popleft()[0])

        if not ready_queue and waiting_queue:
            gantt_chart.append(("no process", time, waiting_queue[0][1]))
            time = waiting_queue[0][1]

        if time == previous_time:
            idle_iterations += 1
        else:
            idle_iterations = 0  # Reset if progress is made

        if idle_iterations >= max_idle_iterations:
            # Free all resources
            for resource_id in resource_flags:
                resource_flags[resource_id] = 1
                resource_holdings[resource_id] = None
            # Move all waiting processes to the ready queue
            while resource_waiting_queue:
                ready_queue.append(resource_waiting_queue.popleft()[0])
            idle_iterations = 0  # Reset counter after recovery

    return gantt_chart, completed_processes, process_waiting_times


def calculate_times(completed_processes, gantt_chart, process_waiting_times):
    turnaround_times = {}
    completion_times = {}

    # Calculate completion time for each process based on the Gantt chart
    for entry in gantt_chart:
        if entry[0] != "no process":
            pid = entry[0]
            completion_times[pid] = entry[2]

    # Calculate turnaround time for each process
    for process in completed_processes:
        pid = process['PID']
        arrival_time = process['Arrival Time']
        turnaround_times[pid] = completion_times[pid] - arrival_time

    # Calculate average waiting time and average turnaround time
    avg_waiting_time = sum(process_waiting_times.values()) / len(process_waiting_times)
    avg_turnaround_time = sum(turnaround_times.values()) / len(turnaround_times)

    return process_waiting_times, turnaround_times, avg_waiting_time, avg_turnaround_time


# Main execution
filename = 'input.txt'
quantum = 10
processes =read_input_file(filename)
print("Initial Processes:")
for process in processes:
    print(process)

gantt_chart, completed_processes, process_waiting_times = simulate_scheduling(processes, quantum)
waiting_times, turnaround_times, avg_waiting_time, avg_turnaround_time = calculate_times(completed_processes, gantt_chart, process_waiting_times)

print("\nGantt Chart:")
print(gantt_chart)
print("\nWaiting Times:", waiting_times)
print("Turnaround Times:", turnaround_times)
print("Average Waiting Time:", avg_waiting_time)
print("Average Turnaround Time:", avg_turnaround_time)



#Ibrahim Salahat                                                         
# 1221701
#Sadeen Faqeeh                                                            
# 1222177
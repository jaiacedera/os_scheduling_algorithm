class Process:
    def __init__(self, pid, at, bt, priority=0):
        self.pid = pid
        self.at = at
        self.bt = bt
        self.rt = bt
        self.priority = priority
        self.st = -1
        self.et = 0
        self.wt = 0
        self.tat = 0
        self.completed = False

    def compute_times(self, current_time):
        self.et = current_time
        self.tat = self.et - self.at
        self.wt = self.tat - self.bt

def insert_idle_slots(gantt):
    if not gantt:
        return gantt
    new_gantt = [gantt[0]]
    for i in range(1, len(gantt)):
        prev_end = new_gantt[-1][2]
        curr_start = gantt[i][1]
        if curr_start > prev_end:
            new_gantt.append(("Idle", prev_end, curr_start))
        new_gantt.append(gantt[i])
    return new_gantt

def fcfs(processes):
    processes.sort(key=lambda p: p.at)
    time = 0
    gantt = []
    for p in processes:
        if time < p.at:
            gantt.append(("Idle", time, p.at))
            time = p.at
        p.st = time
        time += p.bt
        p.compute_times(time)
        gantt.append((f"P{p.pid}", p.st, p.et))
    return gantt

def sjf_np(processes):
    time, completed = 0, 0
    gantt = []
    while completed < len(processes):
        ready = [p for p in processes if p.at <= time and not p.completed]
        if not ready:
            time += 1
            continue
        current = min(ready, key=lambda p: p.bt)
        current.st = time
        time += current.bt
        current.compute_times(time)
        current.completed = True
        gantt.append((f"P{current.pid}", current.st, current.et))
        completed += 1
    return insert_idle_slots(gantt)

def srtf(processes):
    time = 0
    completed = 0
    gantt = []
    last_pid = -1
    start_time = None
    while completed < len(processes):
        available = [p for p in processes if p.at <= time and p.rt > 0]
        if not available:
            if last_pid != "Idle":
                if start_time is not None and last_pid != -1:
                    gantt.append(("Idle" if last_pid == "Idle" else f"P{last_pid}", start_time, time))
                start_time = time
                last_pid = "Idle"
            time += 1
            continue
        # Use correct SRTF tie-breaking: remaining time, then arrival, then PID
        current = min(available, key=lambda p: (p.rt, p.at, p.pid))
        if current.st == -1:
            current.st = time
        if current.pid != last_pid:
            if last_pid != -1 and start_time is not None:
                gantt.append(("Idle" if last_pid == "Idle" else f"P{last_pid}", start_time, time))
            start_time = time
            last_pid = current.pid
        current.rt -= 1
        time += 1
        if current.rt == 0:
            current.compute_times(time)
            current.completed = True
            completed += 1
    if start_time is not None:
        gantt.append(("Idle" if last_pid == "Idle" else f"P{last_pid}", start_time, time))
    return insert_idle_slots(gantt)

def priority_np(processes):
    time, completed = 0, 0
    gantt = []
    while completed < len(processes):
        ready = [p for p in processes if p.at <= time and not p.completed]
        if not ready:
            time += 1
            continue
        current = min(ready, key=lambda p: p.priority)
        current.st = time
        time += current.bt
        current.compute_times(time)
        current.completed = True
        gantt.append((f"P{current.pid}", current.st, current.et))
        completed += 1
    return insert_idle_slots(gantt)

def priority_p(processes):
    time = 0
    completed = 0
    gantt = []
    last_pid = -1
    start_time = None
    while completed < len(processes):
        available = [p for p in processes if p.at <= time and p.rt > 0]
        if not available:
            if last_pid != "Idle":
                if start_time is not None and last_pid != -1:
                    gantt.append(("Idle" if last_pid == "Idle" else f"P{last_pid}", start_time, time))
                start_time = time
                last_pid = "Idle"
            time += 1
            continue
        current = min(available, key=lambda p: (p.priority, p.at))
        if current.st == -1:
            current.st = time
        if current.pid != last_pid:
            if last_pid != -1 and start_time is not None:
                gantt.append(("Idle" if last_pid == "Idle" else f"P{last_pid}", start_time, time))
            start_time = time
            last_pid = current.pid
        current.rt -= 1
        time += 1
        if current.rt == 0:
            current.compute_times(time)
            current.completed = True
            completed += 1
    if start_time is not None:
        gantt.append(("Idle" if last_pid == "Idle" else f"P{last_pid}", start_time, time))
    return insert_idle_slots(gantt)

def round_robin(processes, quantum):
    time = 0
    i = 0
    queue = []
    gantt = []
    processes.sort(key=lambda p: p.at)
    n = len(processes)
    while i < n or queue:
        while i < n and processes[i].at <= time:
            queue.append(processes[i])
            i += 1
        if not queue:
            time += 1
            continue
        current = queue.pop(0)
        if current.st == -1:
            current.st = time
        exec_time = min(current.rt, quantum)
        gantt.append((f"P{current.pid}", time, time + exec_time))
        time += exec_time
        current.rt -= exec_time
        while i < n and processes[i].at <= time:
            queue.append(processes[i])
            i += 1
        if current.rt > 0:
            queue.append(current)
        else:
            current.compute_times(time)
            current.completed = True
    return insert_idle_slots(gantt) 
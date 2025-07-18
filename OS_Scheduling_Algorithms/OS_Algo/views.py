from django.shortcuts import render
from .scheduling import Process, fcfs, sjf_np, srtf, priority_np, priority_p, round_robin

def landing(request):
    return render(request, 'landing.html')

def algorithms(request):
    context = {}
    if request.method == 'POST':
        algo = request.POST.get('algorithm')
        n = int(request.POST.get('num_processes'))
        start_pid = int(request.POST.get('starting_pid'))
        at_list = list(map(int, request.POST.get('arrival_time').split()))
        bt_list = list(map(int, request.POST.get('burst_time').split()))
        priority_list = [0] * n
        quantum = None
        if algo in ['npp', 'pp']:
            priority_list = list(map(int, request.POST.get('priority').split()))
        if algo == 'rr':
            quantum = int(request.POST.get('q'))
        processes = [
            Process(start_pid + i, at_list[i], bt_list[i], priority_list[i])
            for i in range(n)
        ]
        if algo == 'fcfs':
            gantt = fcfs(processes)
        elif algo == 'sjf':
            gantt = sjf_np(processes)
        elif algo == 'srtf':
            gantt = srtf(processes)
        elif algo == 'npp':
            gantt = priority_np(processes)
        elif algo == 'pp':
            gantt = priority_p(processes)
        elif algo == 'rr':
            gantt = round_robin(processes, quantum)
        # Prepare table data
        table = []
        for p in sorted(processes, key=lambda x: x.pid):
            row = {
                'pid': p.pid,
                'at': p.at,
                'bt': p.bt,
                'st': p.st,
                'et': p.et,
                'wt': p.wt,
                'tat': p.tat,
            }
            if algo in ['npp', 'pp']:
                row['priority'] = p.priority
            table.append(row)
        total = len(processes)
        total_wt = sum(p.wt for p in processes)
        total_tat = sum(p.tat for p in processes)
        awt = total_wt / total if total else 0
        atat = total_tat / total if total else 0
        context.update({
            'algo': algo,
            'table': table,
            'gantt': gantt,
            'awt': awt,
            'atat': atat,
            'quantum': quantum,
        })
    return render(request, 'algorithms.html', context)

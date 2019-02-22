#
# Author: Kamalesh Babulal <kamalesh@linux.vnet.ibm.com>
# 
# Collect the SPURR statistics for every task.
#
#!/usr/bin/python
from pyroute2 import TaskStats
from pprint import pprint as pp
import os, fnmatch, psutil

ts = TaskStats()
ts.bind()
tasks = {}
cpus = {}
total_cpus = 0

with open('/proc/cpuinfo', 'r') as f:
	for line in f.readlines():
		if line.startswith('processor'):
			cpu = line.split()[2]
			cpus[cpu] =[0,  0]
			total_cpus += 1

print(cpus)

for p in psutil.process_iter(attrs=['name', 'status']):
	ret = ts.get_pid_stat(int(p.pid))[0]
	#print(ret)
	#utime_scaled=ret['attrs'][0][1]['attrs'][1][1]['ac_utimescaled']
	utime_scaled=ret['attrs'][0][1]['attrs'][2][1]['ac_utimescaled']
	stime_scaled=ret['attrs'][0][1]['attrs'][2][1]['ac_stimescaled']
	cpu_run_time_scaled=ret['attrs'][0][1]['attrs'][2][1]['cpu_scaled_run_real_total']
	#stime_scaled=ret['attrs'][0][1]['attrs'][1][1]['ac_stimescaled']
	#cpu_run_time_scaled=ret['attrs'][0][1]['attrs'][1][1]['cpu_scaled_run_real_total']
	delta = 0
	tasks [p.pid] = [p.pid, p.info['name'], p.info['status'], p.cpu_num(), utime_scaled, stime_scaled, cpu_run_time_scaled, delta]
#	print(tasks[p.pid])

for x in range(10):
	for p in psutil.process_iter(attrs=['name', 'status']):
		if p.info['status'] == psutil.STATUS_RUNNING:
			ret = ts.get_pid_stat(int(p.pid))[0]
			utime_scaled=ret['attrs'][0][1]['attrs'][2][1]['ac_utimescaled']
			stime_scaled=ret['attrs'][0][1]['attrs'][2][1]['ac_stimescaled']
			cpu_run_time_scaled=ret['attrs'][0][1]['attrs'][2][1]['cpu_scaled_run_real_total']
			tasks [p.pid][6] = cpu_run_time_scaled - tasks [p.pid][6];
			cpus[p.cpu_num()] = [p.cpu_num(), tasks [p.pid][6]]
	total = 0
	for c in cpus:
		print("cpu: ",cpus[c][0], cpus[c][1])
		total = total + cpus[c][1]
	print("consumption: ", (total/total_cpus))

ts.close()

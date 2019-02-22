#
# Author: Kamalesh Babulal <kamalesh@linux.vnet.ibm.com>
# 
# Collect the SPURR statistics for every CPU.
#
#!/usr/bin/python

import os, fnmatch, time, struct,  binascii
import sys

output_stream = sys.stdout

cpus = {}

def read_spurr(cpu):
	with open('/sys/devices/system/cpu/cpu'+cpu+'/spurr') as f:
		spurr = int(f.readline().rstrip('\n'), 16)
	return spurr

def read_cpu_nominal_freq(cpu):
	with open('/sys/devices/system/cpu/cpu'+cpu+'/cpufreq/cpuinfo_nominal_freq') as f:
		cpu_nominal_freq = int(f.readline().rstrip('\n'), 10)
	return cpu_nominal_freq
		
def read_cpu_cur_freq(cpu):
	with open('/sys/devices/system/cpu/cpu'+cpu+'/cpufreq/cpuinfo_cur_freq') as f:
		cpu_cur_freq = int(f.readline().rstrip('\n'), 10)
	return cpu_cur_freq

with open('/proc/cpuinfo', 'r') as f:
	for line in f.readlines():
		if line.startswith('processor'):
			cpu = line.split()[2]
			spurr = read_spurr(cpu)
			cpu_nominal_freq = read_cpu_nominal_freq(cpu)
			cpu_cur_freq = read_cpu_cur_freq(cpu)
			cpus[cpu] = [spurr, cpu_nominal_freq, cpu_cur_freq]
	print(cpus)

for key, value in cpus.items():
    spurr = read_spurr(key)
    delta_spurr = spurr - value[0]
    cpu_nominal_freq = read_cpu_nominal_freq(cpu)
    cpu_cur_freq = read_cpu_cur_freq(cpu)
    fr = cpu_cur_freq / cpu_nominal_freq 
    #pr_cycles = cpu_cur_freq * 1000000
    pr_cycles = cpu_cur_freq 
    #total_cycles = cpu_nominal_freq * 1000000
    total_cycles = cpu_nominal_freq 
    cr = float(pr_cycles) /float( total_cycles)
    div = float(1000000000 * fr) * float(cr - 1)
    total = float(delta_spurr) / div
    #print(fr, cr, pr_cycles, total_cycles, total)
    print("cpu %3s %.2f\n" % (key, total))
    t = t + total
    cpus[key] = [delta_spurr, cpu_nominal_freq, cpu_cur_freq]
print("=====\n%.2f\n=====\n" % (t))
#print(cpus)

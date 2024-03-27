#############################
# Szeregowanie zadań na pięciu maszynach
# Helena Masłowska 5.12.2023
# 148182
#############################
import sys
import time
from colorama import Fore

# indexes = [144544, 141071, 148058, 148182, 144678, 148199, 145313, 148142, 147306, 148147, 147985, 144331, 145268, 127260]
index = 148182		# Helena
from_who = 148058	# Czyjeś dane
from_who = sys.argv[1]
list_of_ns = [50, 100, 150, 200, 250, 300, 350, 400, 450, 500] ##

machine1, machine2, machine3, machine4, machine5 = [], [], [], [], []
jobs = []

def count_time(output):
	result_time = 0
	for i in range(5):
		actual_time = 0
		if len(output[i]) != 0:
			for j in output[i]:
				p = j[1]
				r = j[2]
				d = j[3]
				m = machine[i]
				if actual_time >= r:
					actual_time += p * m
				else:
					actual_time = r + p * m
				if d >= actual_time:
					result_time += p * m
				else:
					result_time += max(0, p * m - (actual_time - d))
	return result_time

def program(jobs, machines, k):
	#print("jobs:", jobs)
	output = [[], [], [], [], []]
	ready = []
	r_list = [jobs[2] for jobs in jobs]
	r_list = list(set(r_list))

	#print ("r_list:", r_list)
	time_m = [0, 0, 0, 0, 0]
	for r in r_list:															# wrzucaj kolejną porcję danych do listy ready
		# print(Fore.RED, "r:", r, Fore.WHITE)
		ready += [job for job in jobs if job[2] == r]							# lista ready, [index, p, r, d]
		values = [] 															# machine, index, value
		for job in ready:
			value = [0,0,0,0,0]
			end_time = [0,0,0,0,0]
			index, p, r, d = job[0], job[1], job[2], job[3]
			#print("p:", p, "r:", r, "d:", d)
																				# policz wartości dla każdej maszyny i wybierz największą dla tego kafelka
			for i in range(5):
				value[i] = max(time_m[i], r) + p * machines[i] if max(time_m[i], r) + p * machines[i] <= d else (max(time_m[i], r) + p * machines[i]) - ( (max(time_m[i], r) + p * machines[i]) - d )*k
				#print ("value", i, ":", value[i])

			max_value = max(value) 												# gdzie kafelek będzie dawał największą wartość
			machine_index = value.index(max_value)
			values.append([machine_index] + [index] + [max_value])
			#print("values:", values)

			for i in range(5):													# policz czas dla każdej maszyny
				end_time[i] = max(time_m[i], r) + p * machines[i]
				# print("end_time", i, ":", end_time[i])

			# time_m[machine_index] = max(time_m[machine_index], r) + p * machines[machine_index]
			
		# 	print("time_m1:", time_m[0])
		# 	print("time_m2:", time_m[1])
		# 	print("time_m3:", time_m[2])
		# 	print("time_m4:", time_m[3])
		# 	print("time_m5:", time_m[4])
		# print(Fore.YELLOW, "END OF READY", Fore.WHITE)
		
		values.sort(key=lambda x: x[2], reverse=True)							# posortuj wartości malejąco
		# print("values:", values)
		values_to_insert = []													# lista wartości do wstawienia

		# find unique values
		for job in values:
			if job[0] not in [i[0] for i in values_to_insert]:
				values_to_insert.append(job)

		#remove all negative values
		values_to_insert = [job for job in values_to_insert if job[2] >= 0]
		#print("values_to_insert:", values_to_insert)

		# insert values to several machines at the same time
		for machine_id, index, _ in values_to_insert:
			# find index of job in jobs which is equal value_to_insert
			job_index = [job[0] for job in jobs].index(index)
			job_i = jobs[job_index]
			# print("job_i:", job_i)
			# append job to output
			output[machine_id].append(job_i)
			time_m[machine_id] = max(time_m[machine_id], job_i[2]) + job_i[1] * machines[machine_id]

		#for id, i in enumerate(output):
		#	print("output", id, ":", i)

		# get id of jobs to remove
		ids_to_remove = [index for machine, index, value in values_to_insert]
		#print("ids_to_remove:", ids_to_remove)
		# remove jobs from ready
		ready = [job for job in ready if job[0] not in ids_to_remove]
	
	# print("ready:", [ready])
	# sort ready by d
	ready.sort(key=lambda x: x[3], reverse=True)

	# add jobs which are in ready to output
	for i in range(0, len(ready), 5):
		if i <= len(ready)-1:
			job_index = [job[0] for job in jobs].index(ready[i][0])
			job_i = jobs[job_index]
			output[0].append( job_i )
			time_m[0] = max(time_m[0], job[2]) + job[1] * machines[0]
		if i+1 <= len(ready)-1:
			job_index = [job[0] for job in jobs].index(ready[i+1][0])
			job_i = jobs[job_index]
			output[1].append( job_i )
			time_m[1] = max(time_m[1], job[2]) + job[1] * machines[1]
		if i+2 <= len(ready)-1:
			job_index = [job[0] for job in jobs].index(ready[i+2][0])
			job_i = jobs[job_index]
			output[2].append( job_i )
			time_m[2] = max(time_m[2], job[2]) + job[1] * machines[2]
		if i+3 <= len(ready)-1:
			job_index = [job[0] for job in jobs].index(ready[i+3][0])
			job_i = jobs[job_index]
			output[3].append( job_i )
			time_m[3] = max(time_m[3], job[2]) + job[1] * machines[3]
		if i+4 <= len(ready)-1:
			job_index = [job[0] for job in jobs].index(ready[i+4][0])
			job_i = jobs[job_index]
			output[4].append( job_i )
			time_m[4] = max(time_m[4], job[2]) + job[1] * machines[4]
	return output # list of jobs (lists) for each machine # [   [[ 1, 2, 3, 4], [6, 7, 8, 9]],    [[11, 12, 13, 14], [16, 17, 18, 19]] ...]

for n in list_of_ns: 
	f = open("in_"+str(from_who) + "_" + str(n) + ".txt", "r")
	
	n = int(f.readline())
	machine = list(map(float, f.readline().split()))
	jobs = []
	for i in range(n):
		jobs.append(list(map(int, [i+1]+f.readline().split())))
	f.close()

	timer = time.time()
	jobs.sort(key=lambda x: x[3])
	jobs.sort(key=lambda x: x[2])
	output = program(jobs, machine, 0)
	result_time = count_time(output)
	for k in range(1,100):		
		output_new = program(jobs, machine, k)
		result_time_new = count_time(output_new)
		if result_time_new > result_time:
			result_time = result_time_new
			output = output_new
	timer = time.time() - timer
	print("n:", n, "\tresult:", round(result_time, 2), "\ttime:", round(timer, 2), "s")

	f = open("out_" + str(from_who) + "_" + str(index) + "_" + str(n) + ".txt", "w")
	f.write(str(round(result_time, 2)) + "\n")
	for m in output:
		for j in range(len(m)):
			if j != len(m)-1: 	f.write(str(m[j][0]) + " ")
			else: 				f.write(str(m[j][0]))
		f.write("\n")
	f.write(str(round(timer*1000, 2)))
	f.close()

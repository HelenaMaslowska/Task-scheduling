from colorama import Fore

index = 147306			# Helena
from_who = 147306		# Czyjeś dane

machine = []
jobs = []
for n in [50, 250, 500]: ## 50, 100, 150, 200, 250, 300, 350, 400, 450, 
	f_input = open("in_" + str(index) + "_" + str(n) + ".txt", "r")
	f_machines = open("out_" + str(from_who) + "_" + str(index) + "_" + str(n) + ".txt", "r")

	# read result, list of machines from in_file
	n = int(f_input.readline())
	print(Fore.YELLOW + "n:", n, end="\t")	
	machine = list(map(float, f_input.readline().split()))
	
	# read jobs from in_file
	jobs = []
	for i in range(n):
		jobs.append(list(map(int, [i+1]+f_input.readline().split())))
	f_input.close()

	# read output from out_file
	output = []
	result = float(f_machines.readline())
	for i in range(5):
		output.append(list(map(int, f_machines.readline().split())))
	f_machines.close()
	result_time = 0
	for i in range(5):
		actual_time = 0
		for j in output[i]:
			p = jobs[j-1][1]
			r = jobs[j-1][2]
			d = jobs[j-1][3]
			m = machine[i]
			# print(Fore.YELLOW, "p:", p, "r:", r, "d:", d, "m:", m)
			
			if actual_time >= r:
				actual_time += p * m
			else:
				actual_time = r + p * m

			if d >= actual_time:
				result_time += p * m
			else:
				result_time += max(0, p * m - (actual_time - d))
	result_time = round(result_time, 2)

	count_out = sum([len(output[i]) for i in range(5)])
	print(Fore.LIGHTYELLOW_EX, "n:" + Fore.LIGHTYELLOW_EX, count_out, end="\t")

	print(Fore.WHITE, "Value:" + Fore.CYAN, result_time, end="")

	if result_time == result:
		print(Fore.GREEN, "- OK")
	else:	
		print(Fore.RED, "- NOT OK,", result, "should be", result_time)
	print(Fore.RESET, end="")
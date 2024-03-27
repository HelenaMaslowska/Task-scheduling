#############################
# Szeregowanie zadań na trzech maszynach typu Open Shop
# Helena Masłowska 29.12.2023
# 148182
#############################

# dane wejsciowe
#  n
# 1p1 p2 p3 r
# 2p1 p2 p3 r
# 3p1 p2 p3 r
# 4p1 p2 p3 r
# 5p1 p2 p3 r

# wyjscie 
# C
# M1:  1p1 2p1 3p1 4p1 5p1
# M2:  p2 p2 p2 p2 p2
# M3:  p3 p3 p3 p3 p3

from operator import itemgetter
import sys
from colorama import Fore
import time

#IN_LIST [48, 9, 4, 89, 48]
P_INDEX = 0
P1 = 1
P2 = 2
P3 = 3
R = 4

#P1_LIST [23, 2]
T = 1
READY = 2

# tu dodam fora na każdą iterację
from_who = sys.argv[1]
list_of_ns = [50, 100, 150, 200, 250, 300, 350, 400, 450, 500]
for n in list_of_ns:
	filename_in = "in/in_" + str(from_who) + "_" + str(n) + ".txt"
	filename_out = "out/out_" + str(from_who) + "_148182_" + str(n) + ".txt"
	read_file = open(filename_in, "r")
	n = int(read_file.readline())

	in_list = []
	M1_list = [ 0 for _ in range(n) ]
	M2_list = [ 0 for _ in range(n) ]
	M3_list = [ 0 for _ in range(n) ]
	t1_list = [ 0 for _ in range(n) ]
	t2_list = [ 0 for _ in range(n) ]
	t3_list = [ 0 for _ in range(n) ]

	if n not in [4, 50, 100, 150, 200, 250, 300, 350, 400, 450, 500]: 	print("Bledne dane wejsciowe, zegnam!")
	else: 
		for index in range(n): 											in_list.append(list(map(int, [index] + read_file.readline().split())))
		if len(in_list) != n: 											print("Brak wszystkich instancji w in")
		else:
			timer = time.time()
			# TODO: takiego fora tu dam że bedzie wykonywał się 30 razy losując kolejność i wybierze najlepszy wynik XD, bedzie też losował kolejność wewnątrz, P1, P2, P3
			for i in range(n):
				# algorytm - tu decyduje się kolejność
				in_list = sorted(in_list, key=itemgetter(P_INDEX), reverse=True)
				M1_list[i] = [in_list[i][P_INDEX], in_list[i][P1], in_list[i][R]]
				M2_list[i] = [in_list[i][P_INDEX], in_list[i][P2], in_list[i][R]]
				M3_list[i] = [in_list[i][P_INDEX], in_list[i][P3], in_list[i][R]]
				# koniec algorytmu

				# obliczenia czasu dla każdego p i każdej maszyny - tu oblicza się czas
				if i == 0:
					t1_list[i] = M1_list[i][READY]
					t2_list[i] = M2_list[i][READY] + M1_list[i][T]
					t3_list[i] = M3_list[i][READY] + M1_list[i][T] + M2_list[i][T]
				
				else:
					
					current_ready_1 = M1_list[i][READY]
					prev_readyAndP_1 = t1_list[i-1] + M1_list[i-1][T]
					t1_list[i] = max([current_ready_1, prev_readyAndP_1])
					
					current_ready_2 = M2_list[i][READY] + M1_list[i][T]
					prev_readyAndP_2 = t2_list[i-1] + M2_list[i-1][T]
					t2_list[i] = max([current_ready_2, prev_readyAndP_2])
					current_ready_3 = M3_list[i][READY] + M1_list[i][T] + M2_list[i][T]
					prev_readyAndP_3 = t3_list[i-1] + M3_list[i-1][T]
					t3_list[i] = max([current_ready_3, prev_readyAndP_3])
					# print("current_ready_1: ", current_ready_1)
					# print("prev_readyAndP_1: ", prev_readyAndP_1)
					# print("t1_list[i]: ", t1_list[i])
					# print("current_ready_2: ", current_ready_2)
					# print("prev_readyAndP_2: ", prev_readyAndP_2)
					# print("t2_list[i]: ", t2_list[i])
					# print("current_ready_3: ", current_ready_3)
					# print("prev_readyAndP_3: ", prev_readyAndP_3)
					# print("t3_list[i]: ", t3_list[i])
					
				# koniec obliczeń czasu
					
			# obliczenia Cmax
			Cmax = t3_list[n-1] + M3_list[n-1][T]		
			print(in_list)
			print(M1_list)
			print(M2_list)
			print(M3_list)
			print(t1_list)
			print(t2_list)
			print(t3_list)
			print("n: ", n)
			print("Cmax: ", Cmax)
			print("Czas wykonania algorytmu: ", time.time() - timer)
	read_file.close()
	# zapis do pliku
	write_file = open(filename_out, "w")
	write_file.write(str(Cmax) + "\n")
	M1_list = sorted(M1_list, key=itemgetter(P_INDEX))
	M2_list = sorted(M2_list, key=itemgetter(P_INDEX))
	M3_list = sorted(M3_list, key=itemgetter(P_INDEX))
	for i in range(n-1, -1, -1):
		write_file.write(str( t1_list[i] ) + " ")
	write_file.write("\n")
	for i in range(n-1, -1, -1):
		write_file.write(str( t2_list[i] ) + " ")
	write_file.write("\n")
	print("M3_list: ", len(t3_list))
	for i in range(n-1, -1, -1):
		write_file.write(str( t3_list[i] ) + " ")
	write_file.write("\n")
	write_file.close()
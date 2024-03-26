import sys
#filename = "in_148058_500.txt"
out_filename = sys.argv[1]
filename = sys.argv[2]
if filename[:4] == "out_":
	filename, out_filename = out_filename, filename
pairs = []
matrix = []
time = 0
#with open("out_" +  filename.split("_")[1] + "_" + filename.split("_")[2] ) as f:
with open(out_filename) as f:
	line = f.readline()
	late = int(line)
	print(late)
	
	seq = [int(x)-1 for x in f.readline().split()]
	print(seq)
	
	time = float(f.readline())
	print(time)

with open(filename) as f: #in_148058_500.txt
	n = int(f.readline())
	
	for _ in range(n):
		pairs.append([int(x) for x in f.readline().split()])
	
	for _ in range(n):
		matrix.append([int(x) for x in f.readline().split()])

# check if time is correct
print("Czas: " + str(float(time)) + "ms")
if time / 100 > len(seq):
	print("Nie mieści się w czasie")
else:
	print("Mieści się w czasie")

# check if sequence is correct
checksum = pairs[seq[0]][0]
how_much_late = 0
for i in range(1, len(seq)):
	due_time = pairs[seq[i]][1]
	checksum += matrix[seq[i-1]][seq[i]] + pairs[seq[i]][0]

	if checksum > due_time:
		how_much_late += 1

print("Spóźnienia: " + str(how_much_late))
if how_much_late == late:
	print("Prawidłowa liczba spóźnień")
else:
	print("Nieprawidłowa liczba spóźnionych elementów: " + str(late) + " (odebrane) != " + str(how_much_late) + " (obliczone)")

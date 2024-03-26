### ZADANIE
# Uporządkuj elementy w liście tak, by jak najmniej z nich się spóźniało.
# Wejście - pobierz dane z pliku in_148182_50.txt

from colorama import Fore
import time
import sys

filename = sys.argv[1]
# filename = "in_148058_500.txt"

segments = filename.split("_")
out_filename = "out_" + segments[1] + "_148182_" + segments[2]

n = 0				# liczba elementów
pairs = []			# para: [numer, czas przygotowania, czas zakończenia]
matrix = []			# macierz: każdy wiersz oznacza jeden element, po którym kolejne elementy mają gap

# Wczytanie danych z pliku
with open(filename) as f:
	line = f.readline()
	n = int(line)

	for i in range(n):
		line = f.readline()
		pairs.append([i] + [int(x) for x in line.split()])
	
	for _ in range(n):
		line = f.readline()
		matrix.append([int(x) for x in line.split()])

start_time = time.time()
# Sortowanie po czasie zakończenia
pairs.sort(key=lambda x: x[2])


# Stwórz tablicę kolejnych indeksów
indexes = [x[0] for x in pairs]
skipped = []


# Stwórz tablicę [   previous gap   ] + [   current time   ] + [   next gap   ]
values = [pairs[0][1] + matrix[indexes[0]][indexes[1]]] 		# pierwszy element to [   curr time   ] + [   gap   ]
# print(values, "pair time:", pairs[0][1], ", id next:",indexes[1], ", next gap:", matrix[indexes[0]][indexes[1]])
for i in range(1, n-1):
	values.append(matrix[indexes[i-1]][indexes[i]] + pairs[i][1] + matrix[indexes[i]][indexes[i+1]] - matrix[indexes[i-1]][indexes[i+1]])
	# print(values, "prev id:", indexes[i-1], "curr id:", indexes[i], "next id:", indexes[i+1])
	# print("prev gap:", matrix[indexes[i-1]][indexes[i]], "curr time:", pairs[i][1], "next gap:", matrix[indexes[i]][indexes[i+1]])
values.append(matrix[indexes[n-2]][indexes[n-1]] + pairs[n-1][1])
# print(values, "prev id:", indexes[n-2], "curr id:", indexes[n-1])


# Czasy zakończenia gdyby istniał element o danym indeksie w tej tablicy [   previous sum   ] + [   gap   ] + [   current time   ]
sums = [pairs[0][1]]
# print(sums)
for i in range(1, n):
	sums.append(sums[i-1] + matrix[indexes[i-1]][indexes[i]] + pairs[i][1])
	# print(sums, "prev id:", indexes[i-1], "curr id:", indexes[i], "prev gap:", matrix[indexes[i-1]][indexes[i]], "curr time:", pairs[i][1])


# Wyrzucanie elementu który w tablicy values ma największą wartość
# print("pary:", pairs)				# > 0, > 0, > 0
# print("\nindexes:", indexes)		# > 0,     <---------------    	niezależne, każde -1 to usunięty element
# print("\nvalues:", values)			# Naturalne						niezależne, każde -1000000 to usunięty element
# print("\nsums", sums)				# > 0							zależne, każde -1 to usunięty element
# print()
i = 0
while i < n:
	if indexes[i] < 0:
		#print(Fore.RED, "niemożliwe", Fore.RESET)
		print("", end="")
	else:
		# print(Fore.YELLOW, i, indexes[i], "porównuję", sums[i], ">", pairs[i][2])
		# print(Fore.RESET, end="")
		# print("jeśli ok to zostawiam", indexes[i], "bo", sums[i], "<=", pairs[i][2], "gap:", )
		if sums[i] > pairs[i][2]:
			max_index = values.index(max(values[:i+1]))
			# print(Fore.RED, "skipped", i, "bo", sums[i], ">", pairs[i][2], "max_index:", max_index, Fore.RESET)
			
			# if indexes[max_index] < 0:  print(Fore.RED, "               max_index < 0              ", values[max_index], indexes[max_index], max_index, Fore.RESET)
			
			skipped.append(indexes[max_index])
			# print("SKIPPED                                               ",skipped)
			# print("usuwam", indexes[max_index], "bo", values[max_index], "jest największe")
			# pary zostawiam, indeksy ustawiam na -1, sumy ustawiam na -1, wartości indexu na -1 a poboczne aktualizuję
			indexes[max_index] = -1
			sums[max_index] = -1
			values[max_index] = -1
			curr_pos = 0
			last_pos = n-1

			for k in range(len(indexes[:i+1])):
				if indexes[k] >= 0:
					curr_pos = k								# pierwsza wartość nieujemna, czyli pierwsza na liście działających
					break
			for k in range(n-1, 0, -1):
				#print("k:", k, "indexes[k]:", indexes[k])
				if indexes[k] >= 0:
					last_pos = k
					break
			# print("pierwszy działający:", curr_pos)
			# print("ostatni działający:", last_pos)

			# print("\nindexes:", indexes)		# > 0,     <---------------    	niezależne, każde -1 to usunięty element
			# print("\nvalues:", values)			# Naturalne						niezależne, każde -1000000 to usunięty element
			# print("\nsums", sums)	
			
			# aktualizacja sum
			sums[curr_pos] = pairs[curr_pos][1]
			# print("sums:","ustawiam", curr_pos, "na", pairs[curr_pos][1])

			prev_pos = curr_pos 					# INDEKS 0,1,2,3, ustaw na ostatni_dzialajacy bo na początku na 100% wiemy że ostatni_dzialajacy > 0, poprzedni for
			pos = curr_pos + 1 						# INDEKS 0,1,2,3, ustaw na następny element, w while sprawdzamy czy nie jest przypadkiem -1
			while pos < n:
				if indexes[pos] >= 0:
					sums[pos] = sums[prev_pos] + matrix[indexes[prev_pos]][indexes[pos]] + pairs[pos][1]
					prev_pos = pos
				pos += 1

			# aktualizacja values
			# przypadek gdy wyrzucana wartość jest pierwsza
			# print(Fore.BLUE, "sprawdzam", max_index, "czy jest pierwszy, pierwsza nieujemna", curr_pos, Fore.RESET)
			if max_index == curr_pos:
				pos = curr_pos
				next_pos = curr_pos + 1
				while next_pos < n and indexes[next_pos] < 0: next_pos += 1
				values[pos] = pairs[pos][1] + matrix[indexes[pos]][indexes[next_pos]]

				next_next_pos = next_pos + 1
				while next_next_pos < n and indexes[next_next_pos] < 0: next_next_pos += 1
				values[next_pos] = matrix[indexes[pos]][indexes[next_pos]] + pairs[next_pos][1] + matrix[indexes[next_pos]][indexes[next_next_pos]] - matrix[indexes[pos]][indexes[next_next_pos]]
				# print(Fore.GREEN, "pierwszy values:", "ustawiam", pos, "na", pairs[pos][1] + matrix[indexes[pos]][indexes[next_pos]])
			
			# gdy wyrzucana wartość jest ostatnia
			# print(Fore.BLUE, "sprawdzam", max_index, "czy jest ostatni, ostatnia nieujemna", last_pos, Fore.RESET)
			if max_index == last_pos:
				pos = last_pos
				prev_pos = last_pos - 1
				while prev_pos >= 0 and indexes[prev_pos] < 0: prev_pos -= 1
				values[pos] = matrix[indexes[prev_pos]][indexes[pos]] + pairs[pos][1]

				prev_prev_pos = prev_pos - 1
				while prev_prev_pos >= 0 and indexes[prev_prev_pos] < 0: prev_prev_pos -= 1
				values[prev_pos] = matrix[indexes[prev_prev_pos]][indexes[prev_pos]] + pairs[prev_pos][1] + matrix[indexes[prev_pos]][indexes[pos]] - matrix[indexes[prev_prev_pos]][indexes[pos]]
				# print(Fore.GREEN, "ostatni values:", "ustawiam", pos, "na", matrix[indexes[prev_pos]][indexes[pos]] + pairs[pos][1])

			if max_index != curr_pos and max_index != last_pos:
				# wybierz najwcześniejszego sąsiada
				prev_prev_pos = prev_pos - 1
				prev_pos = max_index - 1
				next_pos = max_index + 1
				next_next_pos = next_pos + 1

				while prev_pos >= 0 and indexes[prev_pos] < 0: prev_pos -= 1
				while prev_prev_pos >= 0 and indexes[prev_prev_pos] < 0: prev_prev_pos -= 1
				while next_pos < n and indexes[next_pos] < 0: next_pos += 1
				while next_next_pos < n and indexes[next_next_pos] < 0: next_next_pos += 1

				if max_index == n-1:
					# print(Fore.BLUE, "to ostatnia wartość", Fore.RESET)
					continue

				if prev_pos == curr_pos:
					# pierwsza wartość nieujemna po wartościach ujemnych
					values[prev_pos] = pairs[prev_pos][1] + matrix[indexes[prev_pos]][indexes[next_pos]] # dla ostatniego pozostałego elementu nie zadziała
					values[next_pos] = matrix[indexes[prev_pos]][indexes[next_pos]] + pairs[next_pos][1] + matrix[indexes[next_pos]][indexes[next_next_pos]] - matrix[indexes[prev_pos]][indexes[next_next_pos]]

				if next_pos == last_pos:
					# ostatnia wartość nieujemna przed wartościami ujemnymi
					values[next_pos] = matrix[indexes[prev_pos]][indexes[next_pos]] + pairs[next_pos][1]
					values[prev_pos] = matrix[indexes[prev_prev_pos]][indexes[prev_pos]] + pairs[prev_pos][1] + matrix[indexes[prev_pos]][indexes[next_pos]] - matrix[indexes[prev_prev_pos]][indexes[next_pos]]

				if prev_pos != curr_pos and next_pos != last_pos:
					# wybierz najwcześniejszego sąsiada
					# print("prev_pos:", prev_pos, "prev_prev_pos:", prev_prev_pos, "next_pos:", next_pos, "next_next_pos:", next_next_pos)
					# aktualizacja sąsiadów
					
					values[prev_pos] = matrix[indexes[prev_prev_pos]][indexes[prev_pos]] + pairs[prev_pos][1] + matrix[indexes[prev_pos]][indexes[next_pos]] - matrix[indexes[prev_prev_pos]][indexes[next_pos]]
					# print(Fore.YELLOW, "values:", "ustawiam", prev_pos, "na", matrix[indexes[prev_prev_pos]][indexes[prev_pos]] + pairs[prev_pos][1] + matrix[indexes[prev_pos]][indexes[next_pos]] - matrix[indexes[prev_prev_pos]][indexes[next_pos]])
					values[next_pos] = matrix[indexes[prev_pos]][indexes[next_pos]] + pairs[next_pos][1] + matrix[indexes[next_pos]][indexes[next_next_pos]] - matrix[indexes[prev_pos]][indexes[next_next_pos]]
					# print(Fore.YELLOW, "values:", "ustawiam", next_pos, "na", matrix[indexes[prev_pos]][indexes[next_pos]] + pairs[next_pos][1] + matrix[indexes[next_pos]][indexes[next_next_pos]] - matrix[indexes[prev_pos]][indexes[next_next_pos]])
					# print(Fore.RESET, end="")
			i -= 1
	i += 1

# nieujemne indeksy to
result = [x for x in indexes if x >= 0]

end_time = time.time()

print("result:", len(result), ":", result)
print("\nlate:", len(skipped), ":", skipped)

# Wypisz wynik
with open(out_filename, 'w') as f:
	f.write(str(len(skipped)) + '\n')
	for x in result+skipped:
		f.write(str(x+1) + ' ')
	f.write('\n')
	f.write( str(round((end_time - start_time)*1000, 4)) )

print("\nSaved to file:", out_filename)
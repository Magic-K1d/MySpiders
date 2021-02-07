import csv

with open('test.csv', encoding='utf8') as csvfile:
	reader = csv.reader(csvfile)
	i = 0

	for row in reader:
		i += 1
	print(i)
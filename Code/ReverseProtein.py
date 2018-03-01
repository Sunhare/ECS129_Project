import sys
protein_name = sys.argv[1]
protein_file = open(protein_name, 'r')

#Output the file contents by using
#python3 ReverseProtein.py 1yvel_original.txt > 1yvel_reversed.txt
#This will create 1yvel_reversed.txt which is the reversed sequence of
#1yvel_original.txt

reverseAA = None

point_array = protein_file.readlines()
reversed_array = point_array[::-1]
reversed_array = list(map(lambda s: s.strip(), reversed_array))

for line in reversed_array:
	print(line)
#KnotAlgorithm.py
from Geometry3D import *

"""Look into MatPlotLib"""


#Open the amino acid sequences
protein_name = input('Enter the name of the protein: ')

protein_file = open(protein_name+'_original.txt', 'r')

#Declare an empty list to store the amino acids along with their coordinates
AA_array = list()

#Used to map the strings of amino acids into floats that python can use for calculations
for amino_acid_coord in protein_file:
	AA = list(map(float, amino_acid_coord.split()))
	AA_array.append(AA)

#The number of triangles we need to create to loop through
num_triangles = len(AA_array)-2 #The last triangle is defined 2 residues away from the last


something_to_do = True #Used to terminate the algorithm
knot_present = None #Initializing if there's a knot present to None, since we don't know

N_moved = 0 #Whenever we make a move, record here
N_could_have_moved = 0 #Whenever we could make a move but don't because we're blocked, record here

#Sanity check variables
num_iters = 0
flat_counter = 0

while something_to_do:
# for index in range(1): #Debugging, Data Visualization
	for i in range(num_triangles):
		blocked = False #Assume not blocked for every triangle

		#Reading frame of 3 amino acids at a time
		AA1 = Point(AA_array[i][0], AA_array[i][1], AA_array[i][2]) #First residue
		AA2 = Point(AA_array[i+1][0], AA_array[i+1][1], AA_array[i+1][2]) #Second residue
		AA3 = Point(AA_array[i+2][0], AA_array[i+2][1], AA_array[i+2][2]) #Third residue

		ABC = Triangle(AA1, AA2, AA3)

		if ABC.isFlat() == False:

			ABC.tryFlatten()
			ABpB = Triangle(ABC.A, ABC.B_prime, ABC.B)
			CBpB = Triangle(ABC.C, ABC.B_prime, ABC.B)

			#Used to exclude edges of triangles in checking if there's a block; inverted list is a generator
			if AA_array[i-1] != None:
				AA_array_before_i = AA_array[i-1]
			excluded_values = [AA_array_before_i, AA_array[i], AA_array[i+1], AA_array[i+2], AA_array[len(AA_array)-1]]
			inverted_list = (index for (index, element) in enumerate(AA_array) if element not in excluded_values)

			#Checks the rest of the residues as line segments to insure no blockage
			for ind in inverted_list: 

				D = Point(AA_array[ind][0], AA_array[ind][1], AA_array[ind][2]) #Line segment start
				E = Point(AA_array[ind+1][0], AA_array[ind+1][1], AA_array[ind+1][2]) #Line segment end

				DE = Line(D,E)

				#Check if every pair of amino acids is blocking ABC from being flattened
				#If we encounter a block, exit the for loop
				if ABpB.intersected_by_line_segment(DE) or CBpB.intersected_by_line_segment(DE):
					#Debugging
					# print("Intersection Found")
					# print("ABpB intersected by DE: " + str(ABpB.intersected_by_line_segment(DE)))
					# print(ABpB)
					# print("CBpB intersected by DE: " + str(CBpB.intersected_by_line_segment(DE)))
					# print(CBpB)
					# print(DE)
					# print()
					
					blocked = True
					N_could_have_moved += 1
					break

			if not blocked:
				#Changes the main array of amino acids	
				(AA_array[i+1][0], AA_array[i+1][1], AA_array[i+1][2]) =  ABC.B_prime.tuple_form
				N_moved += 1

		else:
			#Actual algorithm deletes a point if it's flat, couldn't manage it here
			# del AA_array[i+1]
			flat_counter += 1
				

	num_iters += 1

	#Algorithm Visualization
	print("Num Iters: " + str(num_iters) + " N_moved " + str(N_moved) +" N_could_have_moved " + str(N_could_have_moved) +" Flat Counter " + str(flat_counter) ) # Debugging 


	# #Debugging, first encountered block
	# if(N_could_have_moved > 0):
	# 	something_to_do = False
	# 	myfile_name = '5pti_folded_'+str(num_iters)+'.txt'
	# 	test_file = open(myfile_name, 'w')
	# 	for item in AA_array:
	# 		test_file.write("%f\t%f\t%f\n" %(item[0], item[1], item[2]))
	# 	test_file.close()

	# Data Visualization
	if N_moved == 0:
		myfile_name = str(protein_name)+'_folded_'+str(num_iters)+'.txt'
		test_file = open(myfile_name, 'w')
		for item in AA_array:
			test_file.write("%f\t%f\t%f\n" %(item[0], item[1], item[2]))
		test_file.close()

	#Program Termination
	if(N_moved == 0):
		something_to_do = False

		if(N_could_have_moved == 0):
			knot_present = False
		else:
			knot_present = True

	N_moved = 0
	N_could_have_moved = 0
	flat_counter = 0

print("Knot Present?: " + str(knot_present))


protein_file.close()

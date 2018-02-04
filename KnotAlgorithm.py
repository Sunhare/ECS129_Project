from Geometry3D_Rewrite import *

#Open the amino acid sequences
protein_file = open('5pti_folded_0.txt', 'r')

#Declare an empty list to store the amino acids along with their coordinates
AA_array = list()

#Used to map the strings of amino acids into floats that python can use for calculations
for amino_acid_coord in protein_file:
	AA = list(map(float, amino_acid_coord.split()))
	AA_array.append(AA)

#The number of triangles we need to create to loop through
#The last triangle is the index 2 away from the length of amino acids we have
num_triangles = len(AA_array)-2


something_to_do = True #Used to terminate the algorithm
knot_present = None #Initializing if there's a knot present to None, since we don't know

K_move = 0 #Whenever we make a move, record here
K_like_to_move = 0 #Whenever we could make a move but don't because we're blocked, record here

#Sanity check variables
num_iters = 0
flat_counter = 0

while something_to_do:
# for index in range(2): #Debugging, Data Visualization
	for i in range(num_triangles):
		blocked = False #Assume not blocked for every triangle

		#Reading frame of 3 amino acids at a time
		AA1 = Point(AA_array[i][0], AA_array[i][1], AA_array[i][2]) #First residue
		AA2 = Point(AA_array[i+1][0], AA_array[i+1][1], AA_array[i+1][2]) #Second residue
		AA3 = Point(AA_array[i+2][0], AA_array[i+2][1], AA_array[i+2][2]) #Third residue

		ABC = Triangle(AA1, AA2, AA3)

		# print(ABC.distance)

		if ABC.isFlat() == False:
			ABC.tryFlatten()
			ABpB = Triangle(ABC.A, ABC.B_prime, ABC.B)
			CBpB = Triangle(ABC.C, ABC.B_prime, ABC.B)

			#Used to exclude edges of triangles in checking if there's a block; inverted list is a generator
			
			if AA_array[i-1] != None:
				AA_array_before_i = AA_array[i-1]
			excluded_values = [AA_array_before_i, AA_array[i], AA_array[i+1], AA_array[i+2], AA_array[len(AA_array)-1]]
			inverted_list = (index for (index, element) in enumerate(AA_array) if element not in excluded_values)

			

			for ind in inverted_list: 

				D = Point(AA_array[ind][0], AA_array[ind][1], AA_array[ind][2]) #Line segment start
				E = Point(AA_array[ind+1][0], AA_array[ind+1][1], AA_array[ind+1][2]) #Line segment end

				DE = Line(D,E)

				#Check if every pair of amino acids is blocking ABC from being flattened
				#If we encounter a block, exit the for loop
				#FIXME: Currently doesn't work, look into how the triangles are flattened
				if ABpB.intersected_by_line_segment(DE) or CBpB.intersected_by_line_segment(DE):
					# print("ABpB intersected by DE: " + str(ABpB.intersected_by_line_segment(DE)))
					# print(ABpB)
					# print(DE)
					# print("CBpB intersected by DE: " + str(CBpB.intersected_by_line_segment(DE)))
					# print(CBpB)
					# print(DE)
					blocked = True
					K_like_to_move += 1
					break
				
				
					

			if not blocked:
				(AA_array[i+1][0], AA_array[i+1][1], AA_array[i+1][2]) =  ABC.B_prime.tuple_form
				K_move += 1

		else: 
			flat_counter += 1
				

	num_iters += 1

	#Algorithm Visualization
	print("Num Iters: " + str(num_iters) + " K_move " + str(K_move) +" K_like_to_move " + str(K_like_to_move) +" Flat Counter " + str(flat_counter) ) # Debugging 


	#Data Visualization
	if K_move == 0:
		myfile_name = '5pti_folded_'+str(num_iters)+'.txt'
		test_file = open(myfile_name, 'w')
		for item in AA_array:
			test_file.write("%f\t%f\t%f\n" %(item[0], item[1], item[2]))
		test_file.close()

	# something_to_do = False #Debugging

	if(K_move == 0):
		something_to_do = False

		if(K_like_to_move == 0):
			knot_present = False
		else:
			knot_present = True

	K_move = 0
	K_like_to_move = 0
	flat_counter = 0

print("Knot Present?: " + str(knot_present))

protein_file.close()

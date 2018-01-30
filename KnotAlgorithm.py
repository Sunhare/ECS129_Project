from Geometry3D import *

"""
TO DO 

Figure out a better triangle.tryFlatten() method
Current one caps out at 45 flat triangles in 200 or so iterations
	for epsilon = 0.9 and the threshold at 2

This is not the behavior I want, I want it to progressively get smaller step size,
which this method does, but I want it to go a little faster.

Current method for flattening the triangle: 
	For a triangle ABC
	Find M, the midpoint of AC
	Find the line in parametric form that describes BM
	Take a parametric step of size epsilon from B toward M 
	The point where you land is updated as B_prime. Both B and B_prime are stored
		for checking if a line segment is blocking us


Just realized that isBlocked is an awful function, would never tell us if there's a block
because B_prime is never updated beforehand

"""

#Open the amino acid sequences
protein_file = open('5pti.txt', 'r')

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
# for index in range(20): #Debugging, Data Visualization

	for i in range(num_triangles):
		blocked = False #Assume not blocked for every triangle

		#Reading frame of 3 amino acids at a time
		AA1 = Point(AA_array[i][0], AA_array[i][1], AA_array[i][2]) #First residue
		AA2 = Point(AA_array[i+1][0], AA_array[i+1][1], AA_array[i+1][2]) #Second residue
		AA3 = Point(AA_array[i+2][0], AA_array[i+2][1], AA_array[i+2][2]) #Third residue

		#I probably should have defined a Plane to be a property of a Triangle, but I didn't
		#So now a Triangle is a property of a Plane
		ABC = Plane(AA1, AA2, AA3)

		#Used to exclude edges of triangles in checking if there's a block; inverted list is a generator
		
		excluded_values = [AA_array[i], AA_array[i+1], AA_array[i+2], AA_array[len(AA_array)-1]]
		inverted_list = (index for (index, element) in enumerate(AA_array) if element not in excluded_values)


		for ind in inverted_list: 
			D = Point(AA_array[ind][0], AA_array[ind][1], AA_array[ind][2]) #Line segment start
			E = Point(AA_array[ind+1][0], AA_array[ind+1][1], AA_array[ind+1][2]) #Line segment end

			DE = Line(D,E)

			#Check if every pair of amino acids is blocking ABC from being flattened
			blocked = isBlocked(ABC, DE)
			

			#If we encounter a block, exit the for loop
			if blocked:
				break

		if ABC.triangle.isFlat():
			flat_counter += 1

		# print(ABC.triangle.squish) #Debugging
		if ABC.triangle.isFlat() == False:
			if not blocked:
				ABC.triangle.tryFlatten()

				#Actually moving the amino acid to the new flat point
				(AA_array[i+1][0], AA_array[i+1][1], AA_array[i+1][2]) =  ABC.triangle.B_prime.tuple_form
				
				K_move += 1

			elif blocked:
				K_like_to_move += 1

	num_iters += 1

	
	print("Num Iters: " + str(num_iters) + " K_move " + str(K_move) +" K_like_to_move " + str(K_like_to_move) +" Flat Counter " + str(flat_counter) ) # Debugging 


	#Data Visualization
	# if flat_counter == 40:	
	# 	myfile_name = '5pti_folded_'+str(num_iters)+'.txt'
	# 	test_file = open(myfile_name, 'w')
	# 	for item in AA_array:
	# 		test_file.write("%f\t%f\t%f\n" %(item[0], item[1], item[2]))
	# 	test_file.close()

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

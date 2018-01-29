from Geometry3D import *

"""
TO DO 

Figure out why triangles aren't flattening, 
and why loop isn't terminating
and why some triangles have two repeated points

"""

protein_file = open('5pti.txt', 'r')

AA_array = list()

for amino_acid_coord in protein_file:
	AA = list(map(float, amino_acid_coord.split()))
	AA_array.append(AA)


# for coord in AA_array:
# 	print(coord)


num_triangles = len(AA_array)-2

something_to_do = True

knot_present = None #Initializing if there's a knot present to None

K_move = 0
K_like_to_move = 0

num_iters = 0
flat_counter = 0
while something_to_do:
	for i in range(num_triangles):
		# print(i)
		blocked = False #Assume not blocked for every triangle

		AA1 = Point(AA_array[i][0], AA_array[i][1], AA_array[i][2]) #First residue
		AA2 = Point(AA_array[i+1][0], AA_array[i+1][1], AA_array[i+1][2]) #Second residue
		AA3 = Point(AA_array[i+2][0], AA_array[i+2][1], AA_array[i+2][2]) #Third residue

		ABC = Plane(AA1, AA2, AA3)

		#Used to exclude edges of triangles in checking if there's a block
		excluded_values = [AA_array[i], AA_array[i+1], AA_array[i+2], AA_array[len(AA_array)-1]]
		generator = (index for (index, element) in enumerate(AA_array) if element not in excluded_values)


		for ind in generator: 
			# print(ind)
			D = Point(AA_array[ind][0], AA_array[ind][1], AA_array[ind][2]) #Line segment start
			E = Point(AA_array[ind+1][0], AA_array[ind+1][1], AA_array[ind+1][2]) #Line segment end

			DE = Line(D,E)

			blocked = isBlocked(ABC, DE)

			#If we encounter a block, exit the for loop
			if blocked:
				break

		# print("Blocked: " + str(blocked) + " isFlat?: " + str(ABC.triangle.isFlat()))
		if ABC.triangle.isFlat(True):
			flat_counter += 1

		if not blocked and not ABC.triangle.isFlat():
			
			ABC.triangle.Flatten()

			#Actually moving the amino acid to the new flat point
			(AA_array[i+1][0], AA_array[i+1][1], AA_array[i+1][2]) =  ABC.triangle.B_prime.tuple_form
			
			K_move += 1

		elif blocked and not ABC.triangle.isFlat():
			K_like_to_move += 1

	num_iters += 1

	#Debugging 
	print("Num Iters: " + str(num_iters) + " K_move " + str(K_move) +" K_like_to_move " + str(K_like_to_move) +" Flat Counter " + str(flat_counter) )

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

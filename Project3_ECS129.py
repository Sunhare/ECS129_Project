from Geometry3D import *

"""
Things to check in the morning: 
How to implement isFlat and Flatten
Check your main loop and if you're thinking about it correctly
	This includes seeing if the modulo while loop is a good idea
	Look at the break cases for how to decide if there's a knot or not

"""


# file_name = input("Enter the name of the protein file including the handle: ")

file_name = '5pti.txt' # Reads in the file with the amino acid sequence

protein = open(file_name, 'r')

amino_acids = list() #Makes an empty list to store the amino acids of the protein

#Couldn't think of a better way to do this.
#With this method we need to iterate over the file an additional time
#Organizes the amino acids into nice coordinates that we can access by index
for amino_acid in protein:
	AA = amino_acid
	AA_coord = list(map( float, AA.split() ))
	amino_acids.append(AA_coord)


K_move = 0
K_like_to_move = 0

iteration_period = len(amino_acids)-2
counter = 0

knot = False
blocked = False

first_loop = True

#Main Loop
while True:
	i = counter%iteration_period #This is a periodic function going from 0 to a maximum of iteration period -1
	print("I: " +str(i))

	#Make the amino acids into points 3 at a time
	AA1 = Point(amino_acids[i][0], amino_acids[i][1], amino_acids[i][2])
	AA2 = Point(amino_acids[i+1][0], amino_acids[i+1][1], amino_acids[i+1][2])
	AA3 = Point(amino_acids[i+2][0], amino_acids[i+2][1], amino_acids[i+2][2])

	# print(str(AA1) + '\n' + str(AA2) + '\n' + str(AA3) + '\n') #Used for debugging

	#The triangle to check (Every plane has a triangle defining it- Plane.triangle)
	ABC = Plane(AA1, AA2, AA3)

	#Check the entire protein to ensure there's no line blocking us
	ABC.triangle.Flatten() 

	for j in range(0, len(amino_acids)-1):
		D = Point(amino_acids[j][0], amino_acids[j][1], amino_acids[j][2])
		E = Point(amino_acids[j+1][0], amino_acids[j+1][1], amino_acids[j+1][2])

		if (D != AA1 or D != AA2) or (E != AA1 or E != AA2): #Making sure you're not using the same line segments
		#as the triangle

			DE = Line(D,E)
			#FIXME Make this a triangle
			ABpB = Plane(AA1, ABC.triangle.B_prime, AA2)
			CBpB = Plane(AA3, ABC.triangle.B_prime, AA2)

			left_triangle_intersected = Line_Segment_Intersecting_Triangle(ABpB, DE) #FIXME
			right_triangle_intersected = Line_Segment_Intersecting_Triangle(CBpB, DE)

			if left_triangle_intersected == True or right_triangle_intersected == True: #If something is blocking us
				blocked = True
				print("There was a block")
				# print(str(ABC.triangle) +'\n'+ str(DE))
				# break


	#If you're not blocked, and the triangle isn't flat, flatten the triangle
	if not blocked and not ABC.triangle.isFlat(): 
		
		amino_acids[i+1][0] = ABC.triangle.B_prime.x
		amino_acids[i+1][1] = ABC.triangle.B_prime.y
		amino_acids[i+1][2] = ABC.triangle.B_prime.z

		K_move += 1

	#If you're blocked and the triangle is not yet flat, take note
	elif blocked and not ABC.triangle.isFlat():
		K_like_to_move += 1

	#After one full iteration, if you haven't made any moves
	if i == 0 :
		
		if K_move == 0 and K_like_to_move == 0:
			knot = False
			break
		elif K_move == 0 and K_like_to_move != 0:
			knot = True
			break

		if first_loop == True:
			K_move = 0
			K_like_to_move = 0
			blocked = False
			first_loop = False

	counter += 1

print("Is there a knot?: " + str(knot))




protein.close()
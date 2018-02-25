#Geometry3D.py
from math import sqrt

class Point(): 
	#Constructor, initialized to the zero vector if no input given
	def __init__(self, x=0, y=0, z=0):
		self.x = x #x_coordinate
		self.y = y #y_coordinate
		self.z = z #z_coordinate

	#Used for when you're printing the object
	def __str__(self):
		return ( "%.3f %.3f %.3f\n" %(self.x, self.y, self.z)) 

	#Overloading addition and subtraction to handle points
	def __add__(self, rhs):
		return Point((self.x+rhs.x), (self.y + rhs.y), (self.z + rhs.z))

	def __sub__(self, rhs):
		return Point((self.x-rhs.x), (self.y - rhs.y), (self.z - rhs.z))

	def __mul__(self, rhs):
		return Point((self.x*rhs), (self.y*rhs), (self.z*rhs))

	def __truediv__(self, rhs):
		return Point((self.x/rhs), (self.y/rhs), (self.z/rhs))

	def __eq__(self, rhs):
		if (self.x == rhs.x) and (self.y == rhs.y) and (self.z == rhs.z):
			return True
		else:
			return False

	def __ne__(self, rhs):
		if (self.x != rhs.x) or (self.y != rhs.y) or (self.z != rhs.z):
			return True
		else:
			return False

	@property
	def tuple_form(self):
		return (self.x, self.y, self.z)


class Vector:
	#Constructor, initialized to the zero vector if no input given
	#A = starting point, B = ending point
	def __init__(self, A = Point(0,0,0), B = Point(0,0,0)):
		# if type(A) != Point or type(B) != Point:
			# print(type(A))
			# print(type(B))
			# raise TypeError('The vector was not initialized with two points')

		self.x = B.x-A.x
		self.y = B.y-A.y
		self.z = B.z-A.z

	#The euclidean length is calculated when called
	@property
	def length(self):
		length = sqrt( (self.x**2 + self.y**2 + self.z**2))
		return length

	def __str__(self):
		return ( "Vector: <%.3f, %.3f, %.3f> " %(self.x, self.y, self.z)) 

	def __add__(self, rhs):
		return Vector(Point(0,0,0), Point((self.x+rhs.x), (self.y + rhs.y), (self.z + rhs.z)))

	def __sub__(self, rhs):
		return Vector(Point(0,0,0), Point((self.x-rhs.x), (self.y - rhs.y), (self.z - rhs.z)))

	def __mul__(self,scalar):
		new_position = Point(self.x, self.y, self.z)*scalar
		return Vector(Point(0,0,0), new_position) #Origin to the new scaled position

	def __truediv__(self, rhs):
		return Vector(Point(), Point((self.x/rhs), (self.y/rhs), (self.z/rhs)))

	def __eq__(self, rhs):
		if (self.x == rhs.x) and (self.y == rhs.y) and (self.z == rhs.z):
			return True
		else:
			return False

	def __ne__(self, rhs):
		if (self.x != rhs.x) or (self.y != rhs.y) or (self.z != rhs.z):
			return True
		else:
			return False

	#Dot Product of Self dot Right Hand Side
	def dot(self, rhs):
		return (self.x * rhs.x) + (self.y * rhs.y) + (self.z * rhs.z)

	#Cross Product of Self cross Right Hand Side
	def cross(self, rhs):
		N_x = (self.y * rhs.z) - (rhs.y * self.z)
		N_y = (self.z * rhs.x) - (rhs.z * self.x)
		N_z = (self.x * rhs.y) - (rhs.x * self.y)

		N = Vector(Point(0,0,0), Point(N_x, N_y, N_z)) #Direction vector at origin
		return N

	#Normalizes a vector so it has a length of 1
	def normalize(self):
		tmp = self.length #Since length is a property it's calculated continuously
		if tmp != 0: #Don't divide by zero
			self.x/=tmp
			self.y/=tmp
			self.z/=tmp


class Plane:
	#Constructor, initialized to the zero vector if no input given
	def __init__(self, A=Point(0,0,0), B=Point(0,0,0), C=Point(0,0,0)):
		AB = Vector(A,B)
		AC = Vector(A,C)
		N = AB.cross(AC)
		N.normalize()

		self.a = N.x
		self.b = N.y
		self.c = N.z
		self.d = -1*((self.a * A.x) + (self.b * A.y) + (self.c *A.z))

	#Print the plane equation
	def __str__(self):
		return "Plane: %.2fx + %.2fy + %.2fz + %.2f = 0" %(self.a, self.b, self.c, self.d)
	

class Line:
	def __init__(self, A=Point(0,0,0), B=Point(0,0,0), t=1):
		self.direction = Vector(A,B)
		self.initial_point = A
		self.end_point = B
		self.t = t

	def __str__(self):
		x_comp = str(self.initial_point.x)+' + '+str(self.direction.x) + 't' + '\n'
		y_comp = str(self.initial_point.y)+' + '+ str(self.direction.y) + 't' + '\n'
		z_comp = str(self.initial_point.z)+' + '+str(self.direction.z) + 't' + '\n'
		return "Line:\n" + x_comp + y_comp + z_comp

	#This property is used to find a point on the line given the t parameter
	@property
	def projected_point(self):
		if self.t != None:
			P = Point() #The calculated point
			D = self.initial_point

			#Solving the parametric equation given a value for self.t
			P.x = D.x + self.t*(self.direction.x)
			P.y = D.y + self.t*(self.direction.y)
			P.z = D.z + self.t*(self.direction.z)
			return P

	def plane_intersection(self, P = Plane()):
		#Solving for the point where the line intersects the plane
		try:
			self.t = ((-1*P.d)-(P.a*self.initial_point.x)-(P.b*self.initial_point.y)-(P.c*self.initial_point.z)) / ((P.a*self.direction.x)+(P.b*self.direction.y)+(P.c*self.direction.z))
		except ZeroDivisionError:
			self.t = None
		return self.projected_point 


class Triangle:

	threshold = 0.01 #FIXME Choose a threshold to check if the triangle is flat

	def __init__(self, A=Point(0,0,0), B=Point(0,0,0), C=Point(0,0,0)):
		self.A = A
		self.B = B
		self.C = C

		self.plane = Plane(A, B, C) #Plane created by the triangle

		# self.epsilon = 0.01 #FIXME Chooose an arbitrary epsilon to move flatten the triangle
		
		

	def __str__(self):
		return ("Triangle:\n" + str(self.A)+ str(self.B)+str(self.C))


	@property
	def distance(self):
		AB = Vector(self.A, self.B)
		BC = Vector(self.B, self.C)
		AC = Vector(self.A, self.C)
		
		distance = None

		if AB.dot(AC) <= 0:
			distance = AB.length #B closer to point A but outside segment AC
		elif BC.dot(AC) <= 0:
			distance = BC.length #B closer to point C but outside segment AC
		else:
			distance = (AB.cross(AC).length / AC.length) #B within segment, so perpendicular distance is Area = base * height = 
			#Magnitude of cross product divided by magnitude of base gives us perpendicular height to line
		return distance

	def isFlat(self):
		#Check if point B is less than self.threshold away from the line segment AC
		if self.distance <= Triangle.threshold:
			return True
		else:
			return False

	def tryFlatten(self): 

		#Midpoint Method
		# P = (self.A+ self.C)/2 #Midpoint
		# BP = Vector(self.B, P)
		# BP.normalize() #Makes length of BP == 1
		# BP *= self.epsilon
		# self.B_prime = self.B + BP #Move B in the direction of BP

		#Actual Method Used in Original Journal
		self.B_prime = (self.A+self.B+self.C)/3

	#Uses Barycentric Coordinate Method
	#A is the origin; AB and AC are a basis for any point within the triangle
	#alpha and beta are the coefficients of the basis vectors
	def contains_point(self, P = Point(0,0,0)):
		# P = A + alpha * AC + beta * AB 	# Original equation
		# AP = alpha*AC + beta*AB 			# Subtract A from both sides

		#Take the dot product with both basis vectors to generate 2 equations to solve our system
		# (AP) . AC = (alpha * AC + beta * AB) . AC		
		# (AP) . AB = (alpha * AC + beta * AB) . AB 	

		AP = Vector(self.A, P)
		AB = Vector(self.A, self.B)
		AC = Vector(self.A, self.C)

		# Solving for the coefficients
		alpha = (((AB.dot(AB))*(AP.dot(AC))-(AB.dot(AC))*(AP.dot(AB)))) / (((AC.dot(AC))*(AB.dot(AB)) - (AC.dot(AB))*(AB.dot(AC))))
		beta = (((AC.dot(AC))*(AP.dot(AB))-(AC.dot(AB))*(AP.dot(AC)))) / (((AC.dot(AC))*(AB.dot(AB)) - (AC.dot(AB))*(AB.dot(AC))))

		if (alpha > 0 and beta > 0 and (alpha + beta) < 1):
			return True
		else:
			return False

	#Important function
	def intersected_by_line_segment(self, DE = Line()):
		P = DE.plane_intersection(self.plane) #See where the line spanned by DE intersects the plane made by ABC
		if (DE.t != None) and (DE.t < 1.0 and DE.t > 0.0): #If the lines aren't parallel and the intersection is within the line segment 
			return self.contains_point(P) #Return whether or not the intersection is within the triangle
		else: #If the intersection is not within the line segment, return false
			return False 


#Used to debug Geometry3D
if __name__ == "__main__":
	

#Point Testing
	# A = Point(1, 2, 1)
	# B = Point(-4, -5, 5)
	# C = Point(7, 8, 10)

	# print(A)

	# A4 = B + C
	# print(A4)

	# A5 = C - A
	# print(A5)

	# A6 = A * 2
	# print (A6)

	# A7 = A5/3
	# print(A7)

	# print(A4 == A5)

	# print(B != C)

	# print(A.tuple_form)

#Vector Testing
	# A = Point(1, 2, 1)
	# B = Point(-4, -5, 5)
	# C = Point(7, 8, 10)
	# AB = Vector(A,B)
	# AC = Vector(A,C)
	# BC = Vector(B,C)

	# print(str(AB) + '\n' + str(AC) + '\n' + str(BC))
	# print(AB.length)
	# print(AB + BC)
	# print(BC - AC)
	# print(AB*5)
	# print(BC/7)
	# print(AB == AB)
	# print(AB != BC)

	# print(AB.dot(BC))
	# print(AB.cross(BC))
	# print(BC.normalize())
	# print(BC.normalize().length)

#Plane Testing
	# A = Point(1, 2, 1)
	# B = Point(-4, -5, 5)
	# C = Point(7, 8, 10)

	# ABC = Plane(A,B,C)
	# print(ABC)

#Triangle Testing
	# protein_name = input('Enter the name of the protein: ')
	# print(protein_name)
	# A = Point(0,0,0)
	# B = Point(1.5,1,0)
	# C = Point(2,0,0)

	# ABC = Triangle(A,B,C)
	# print(ABC)

	# print(ABC.isFlat())
	# ABC.tryFlatten()

	# L = Point(0.5,0,1)
	# S = Point(2,1,-1)

	# LS = Line(L,S)
	# print(LS)
	# ABC = Triangle(A,B,C)

	# print(ABC.intersected_by_line_segment(LS))

	A = Point(0,0,0)
	B = Point(1,1,0)
	C = Point(2,0,0)
	D = Point(3,3,0)
	E = Point(4,0,0)
	F = Point(5,2,0)
	G = Point(5,0,0)

	point_array = [A,B,C,D,E,F,G]

	num_triangles = len(point_array)-2

	for i in range(num_triangles):
		# print(point_array[i])

		ABC = Triangle(point_array[i], point_array[i+1], point_array[i+2])
		ABC.tryFlatten()
		print(ABC)











from math import sqrt
import numpy as np



class Point(): 
	#Constructor, initialized to the zero vector if no input given
	def __init__(self, x=0, y=0, z=0):
		self.x = x #x_coordinate
		self.y = y #y_coordinate
		self.z = z #z_coordinate
	#Used for when you're printing the object
	def __str__(self):
		# return ( "Point: (" + str(self.x) + ", " + str(self.y) + ", " + str(self.z) + ")" )
		return ( "Point: (%.3f, %.3f, %.3f) " %(self.x, self.y, self.z)) 
	#Overloading addition and subtraction to handle points
	def __add__(self, rhs):
		assert type(rhs) is Point, "You can only add points to points"
		return (self.x+rhs.x), (self.y + rhs.y), (self.z + rhs.z)
	def __sub__(self, rhs):
		assert type(rhs) is Point, "You can only subtract points from points"
		return (self.x-rhs.x), (self.y - rhs.y), (self.z - rhs.z)


class Vector:
	#Constructor, initialized to the zero vector if no input given
	#A = starting point, B = ending point
	def __init__(self, A = Point(0,0,0), B = Point(0,0,0)):
		if type(A) != Point or type(B) != Point:
			raise TypeError('The vector was not initialized with two points')
		(self.x, self.y, self.z) = B-A #Does B(x,y,z) – A(x,y,z)

	#The euclidean length is calculated when called
	@property
	def length(self):
		length = sqrt( (self.x**2 + self.y**2 + self.z**2))
		return length

	def __str__(self):
		# return ("Vector: <" + str(self.x) + ", " +str(self.y)+", "+str(self.z)+">")
		return ( "Vector: <%.3f, %.3f, %.3f> " %(self.x, self.y, self.z)) 

	def __add__(self, rhs):
		assert type(rhs) is Vector, "You can only add vectors to vectors"
		return (self.x+rhs.x), (self.y + rhs.y), (self.z + rhs.z)

	def __sub__(self, rhs):
		assert type(rhs) is Vector, "You can only subtract vectors from vectors"
		return (self.x-rhs.x), (self.y - rhs.y), (self.z - rhs.z)

	def __mul__(self,scalar):
		new_position = Point(self.x*scalar, self.y*scalar, self.z*scalar)
		return Vector(Point(0,0,0), new_position) #Origin to the new scaled position

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
			self.x /= tmp
			self.y /= tmp
			self.z /= tmp


class Triangle:
	def __init__(self, A=Point(0,0,0), B=Point(0,0,0), C=Point(0,0,0)):
		self.A = A
		self.B = B
		self.C = C

		self.epsilon = 0.003141592657 #FIXME Chooose an arbitrary epsilon to move flatten the triangle
		self.threshold = 0.02 #FIXME Choose a threshold to check if the triangle is flat
		
	def __str__(self):
			return ("Triangle:  A: " + str(self.A) + ", B: " + str(self.B) + ", C: " + str(self.C))

	def isFlat(self): #FIXME Implement this function
		#Check if point B is less than self.threshold away
		# from the line segment AC
		AB = Vector(self.A, self.B)
		CB = Vector(self.C, self.B)
		AC = Vector(self.A, self.B)

		distance = None

		if AB.dot(AC) <= 0:
			distance = AB.length
		elif BC.dot(AC) >= 0:
			distance = BC.length
		else:
			distance =

		return False

		# v = Vector(A, C)
		# w = Vector(A, B)

		# c1 = w.dot(v)
		# if ( c1 <= 0 ):
		# 	return w.length

		# c2 = v.dot(v)
		# if ( c2 <= c1 ):
		# 	return Vector(C, B).length

		# b = c1 / c2;
		# Pb = Point(S.P0 + b * v)
		# return d(P, Pb);

	def Flatten(self): #FIXME implment this function
		#Need to move point B closer to the midpoint
		#of line segment AC by self.epsilon
		pass

	#Check if a point P is inside the triangle
	def is_in_triangle(self, P = Point(0,0,0)):
		A = self.A
		B = self.B
		C = self.C

		AB = Vector(A,B)
		AC = Vector(A,C)
		AP = Vector(A,P)
		BC = Vector(B,C)
		BP = Vector(B,P)

		if np.sign(AB.dot(AC)) == np.sign(AB.dot(AP)):
			if np.sign(AC.dot(AB)) == np.sign(AC.dot(AP)):
				if np.sign(BC.dot(AB*-1)) == np.sign(BC.dot(BP)):
					return True
		return False


class Plane:
	#Constructor, initialized to the zero vector if no input given
	def __init__(self, A=Point(0,0,0), B=Point(0,0,0), C=Point(0,0,0)):
		self.triangle = Triangle(A,B,C)

		AB = Vector(A,B)
		AC = Vector(A,C)
		N = (AB.cross(AC))
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
		self.slope = Vector(A,B)
		self.initial_point = A
		self.end_point = B
		self.t = t

	def __str__(self):
		return "Line: "+str(self.initial_point)+" + t"+str(self.slope)

	#This property is used to find a point on the line given the t parameter

	@property
	def projected_point(self):
		if self.t != None:
			P = Point() #The calculatd point
			D = self.initial_point

			P.x = D.x + self.t*(self.slope.x)
			P.y = D.y + self.t*(self.slope.y)
			P.z = D.z + self.t*(self.slope.z)
			return P

	def plane_intersection(self, P = Plane()):
		A = P.a
		B = P.b
		C = P.c
		D = P.d
		I = self.initial_point

		#Solving for the point where the line intersects the plane
		try:
			self.t = ((-1*D)-(A*I.x)-(B*I.y)-(C*I.z)) / ((A*self.slope.x)+(B*self.slope.y)+(C*self.slope.z))
		except ZeroDivisionError:
			print("The line and the plane appear to be parallel, tried dividing by zero")
			# print(str(self)+",\n"+str(P))
			self.t = None
		return self.projected_point 


#The great function
def Line_Segment_Intersecting_Triangle(ABC = Plane(), DE = Line()):
	P = DE.plane_intersection(ABC) #See where the line spanned by DE intersects the plane made by ABC
	if DE.t != None and DE.t <= 1 and DE.t >= 0: #If the intersection is within the line segment and the lines aren't parallel
		return ABC.triangle.is_in_triangle(P) #Return whether or not the intersection is within the triangle
	else: #If the intersection is not within the line segment, return false
		return False 



#Only executes if Geometry3D is run directly
#Geometry3D Test
if __name__ == "__main__":
	A = Point(0, 4, 0)
	B = Point(4, -4, 0)
	C = Point(-4, -4, 0)


	D = Point(4, -4, 0)
	E = Point(0, 4, 0)

	AB = Vector(A,B)
	ABC = Plane(A,B,C)
	DE = Line(D,E)

	print(A) #Point test
	print(AB) #Vector test
	print(ABC) #Plane test
	print(ABC.triangle) #Triangle test
	print(DE) #Line test
	print(Line_Segment_Intersecting_Triangle(ABC, DE)) #Line Segment intersecting Triangle test



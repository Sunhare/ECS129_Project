from math import sqrt
import numpy as np
#TO DO:
#Raise exceptions if incorrect parameters are passed


class Point: 
	#Constructor, initialized to the zero vector if no input given
	def __init__(self, x=0, y=0, z=0):
		self.x = x #x_coordinate
		self.y = y #y_coordinate
		self.z = z #z_coordinate

	#Used for when you're printing the object
	def __str__(self):
		return ( "(" + str(self.x) + ", " + str(self.y) + ", " + str(self.z) + ")" )

	#Overloading addition and subtraction to handle points
	def __add__(self, rhs):
		return ((self.x+rhs.x), (self.y + rhs.y), (self.z + rhs.z))
	def __sub__(self, rhs):
		return ((self.x-rhs.x), (self.y - rhs.y), (self.z - rhs.z))


class Vector:
	#Constructor, initialized to the zero vector if no input given
	#A = starting point, B = ending point
	def __init__(self, A = Point(), B = Point()):
		(self.x, self.y, self.z) = B-A #Does B(x,y,z) – A(x,y,z)

	#The euclidean length is alculated when called
	@property
	def length(self):
		length = sqrt( (self.x**2 + self.y**2 + self.z**2))
		return length

	def __str__(self):
		return ("<" + str(self.x) + ", " +str(self.y)+", "+str(self.z)+">")

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
		if tmp != 0:
			self.x /= tmp
			self.y /= tmp
			self.z /= tmp


class Triangle:
	def __init__(self, A=Point(), B=Point(), C=Point()):
		self.A = A
		self.B = B
		self.C = C

	#Check if a point P is inside the triangle
	def __str__(self):
			return ("A: " + str(A) + ", B: " + str(B) + ", C: " + str(C))

	def is_in_triangle(self, P = Point()):
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
	def __init__(self, A=Point(), B=Point(), C=Point()):
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
		return "%.2fx + %.2fy + %.2fz + %.2f = 0" %(self.a, self.b, self.c, self.d)
	

class Line:
	def __init__(self, A=Point(), B=Point(), t=1):
		self.slope = Vector(A,B)
		self.initial_point = A
		self.t = t

	def __str__(self):
		return "<r> = "+str(self.initial_point)+" + t"+str(self.slope)

	#This property is used to find a point on the line given the t parameter
	@property
	def projected_point(self):
		P = Point() #The calculatd point

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
		self.t = ((-1*D)-(A*I.x)-(B*I.y)-(C*I.z)) / ((A*self.slope.x)+(B*self.slope.y)+(C*self.slope.z))

		return self.projected_point 


#ABC are the points defining the triangle and the plane
#DE are the points defining the line and line segment
# def Plane_intersection_Line(A, B, C, D, E):


A = Point(0, 4, 0)
B = Point(4, -4, 0)
C = Point(-4, -4, 0)


D = Point(0, 0, 7)
E = Point(0, 0, -1)

print(A,B,C)

AB = Vector(A,B)
print(AB)

ABC = Plane(A,B,C)
print(ABC)

DE = Line(D,E)
print(DE)

P = DE.plane_intersection(ABC)
print(P)
print(DE.t)

print(ABC.triangle)
print(ABC.triangle.is_in_triangle(P))

#The great function
def Line_Segment_Intersecting_Triangle(ABC = Plane(), DE = Line()):
	P = DE.plane_intersection(ABC) #See where the line spanned by DE intersects the plane made by ABC
	if DE.t <= 1 and DE.t >= 0: #If the intersection is within the line segment
		return ABC.triangle.is_in_triangle(P) #Return whether or not the intersection is within the triangle
	else: #If the intersection is not within the line segment, return false
		return False 











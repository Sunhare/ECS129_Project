import math

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
		length = math.sqrt( (self.x**2 + self.y**2 + self.z**2))
		return length

	def __str__(self):
		return ("<" + str(self.x) + ", " +str(self.y)+", "+str(self.z)+">")

	#Dot Product of Self dot Right Hand Side
	def dot(self, rhs):
		return (self.x * rhs.x) + (self.y * rhs.y) + (self.z * rhs.z)

	#Cross Product of Self cross Right Hand Side
	def cross(self, rhs):
		N_x = (self.y * rhs.z) - (rhs.y * self.z)
		N_y = (self.z * rhs.x) - (rhs.z * self.x)
		N_z = (self.x * rhs.y) - (rhs.x * self.y)
		N = Vector(Point(N_x, N_y, N_z))
		return N

	#Normalizes a vector so it has a length of 1
	def normalize(self):
		tmp = self.length #Since length is a property it's calculated continuously
		self.x /= tmp
		self.y /= tmp
		self.z /= tmp



#Line defined by a line segment DE
class Line:
	def __init__(self, D=Point(), E=Point(), t=1):
		self.slope = Vector(D,E)
		self.initial_point = D
		self.t = t

	def __str__(self):
		return "<r> = "+str(self.initial_point)+" + t"+str(self.slope)

	#This method is used to find a point on the line given the t parameter
	# def calculate_point(self, t): #FIX ME find a better name for this method
	# 	M = Point() #The calculatd point

	# 	M.x = D.x + self.t*(self.slope)
	# 	M.y = D.y + self.t*(E.y - D.y)
	# 	M.z = D.z + self.t*(E.z - D.z)
	# 	return M



class Plane:
	#Constructor, initialized to the zero vector if no input given
	def __init__(self, A=Point(), B=Point(), C=Point()):
		AB = Vector(A,B)
		AC = Vector(A,C)
		N = (AB.cross(AC))
		N.normalize()

		self.a = N.x
		self.b = N.y
		self.c = N.z
		self.d = -1*((self.a * A.x) + (self.b * A.y) + (self.c *A.z))

	def __str__(self):
		return "%.2fx + %.2fy + %.2fz + %.2f = 0" %(self.a, self.b, self.c, self.d)

#ABC are the points defining the triangle and the plane
#DE are the points defining the line and line segment
# def Plane_intersection_Line(A, B, C, D, E):


A = Point(2, 4, 6)
B = Point(7, 11, 13)
C = Point(3, 1, 4)


D = Point(4, 1, 8)
E = Point(7, 2, 2)
print(A,B,C)

AB = Vector(A,B)
print(AB)

ABC = Plane(A,B,C)
print(ABC)

DE = Line(D,E)
print(DE)


# print(N.length)


# print(N.length)













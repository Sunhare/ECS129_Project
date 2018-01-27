from Geometry3D import *
#TO DO:
#Raise exceptions if incorrect parameters are passed


#The great function
def Line_Segment_Intersecting_Triangle(ABC = Plane(), DE = Line()):
	P = DE.plane_intersection(ABC) #See where the line spanned by DE intersects the plane made by ABC
	if DE.t <= 1 and DE.t >= 0: #If the intersection is within the line segment
		return ABC.triangle.is_in_triangle(P) #Return whether or not the intersection is within the triangle
	else: #If the intersection is not within the line segment, return false
		return False 



#ABC are the points defining the triangle and the plane
#DE are the points defining the line and line segment
# def Plane_intersection_Line(A, B, C, D, E):


#Test cases
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



print(Line_Segment_Intersecting_Triangle(ABC, DE))






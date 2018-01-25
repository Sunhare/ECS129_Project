import random 
#Takes in the endpoints of a line segment in euclidean space 
#And outputs the Plucker Coordinates which I have to do more research on
#Plucker Coordinates are nice apparently because of the Side-Operator property
#Used to define line segments not centered at the origin
#Which will allow you to tell if two lines are parallel, and if not they intersect
#Parallel if side_operator(a,b) #where a and b are Plucker coordinates# returns 0

#p = tip of line, q = base of line, but I have to confirm that, in my tests cases
#I do the opposite, cause *shrug*
def Plucker_Coordinates(px, py, pz, qx, qy, qz): #Or grassman coordinates? idk
	a0 = px*qy - qx*py;
	a1 = px*qz - qx*pz;
	a2 = px - qx;
	a3 = py*qz - qy*pz;
	a4 = pz-qz;
	a5 = qy - py;

	#This algorithm returns the 2x2 minors of the following matrix:
	#px py pz 1
	#qx qy qz 1
	#Returns 6 member array for side-operator function

	return [a0, a1, a2, a3, a4, a5];


#Takes in two plucker coordinates and returns 0 if they're parallel
#Similar to the dot product, but for lines not centered at the origin
def Side_Operator(a, b):
	side_operator_value = (a[0]*b[4]) + (a[1]*b[5]) + (a[2]*b[3]) + (a[3]*b[2]) + (a[4]*b[0]) + (a[5]*b[1]);
	return side_operator_value;






#Line from (3, 3, 3) to (6, 6, 6)
line_one = Plucker_Coordinates(1, 2, 3, 2 ,2 ,2);

#Line from (-1, -1, -1) to (-3, -3, -3)
line_two = Plucker_Coordinates(-1, -2, -1, -2, -356, 5);

print(line_one);
print(line_two);

if Side_Operator(line_one, line_two) == 0:
	print("The lines are parallel: Side-Operator == 0\n");
else:
	print("The lines intersect somewhere, can't tell you where though. Sorry bud.\n");





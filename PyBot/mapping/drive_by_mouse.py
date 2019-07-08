# just drives to the destinated places
# this is called by the drive_to_pos methode
# all other methodes are just called by this main one.
import a_star
import time
import math
"""
there are 4 pos. ways to drive: forward, backward, left, right. 
(if we take it serious: only 2 ways: forward and backward, for left and right we have to rotate)
to find the position of the new node in reference to the coords of the rob
we use the inverse matrix of ((cos, sin)(-sin, cos))(x,y) = (node_to_go_x, n_t_g_y)
So we do not have to change our orientation of the robot before driving. 
We can just cruise alonge. 
"""
def drive(rob, start, end):
	#go down or in negative x 
	if end[0] < start[0]:
		print("I am driving down")
		#turn around:
		#dest yaw is the yaw at this moment plus die half of the full circle. this mod full circle. 
		dest_yaw = (rob.yaw_angle.value + (rob.circle_value/2) ) % rob.circle_value
		#turn around is done right. So the yaw keeps rising. does only work if it is not 0 
		while rob.yaw_angle.value > dest_yaw or rob.yaw_angle.value==0:
			rob.rightturn(0.001)
			time.sleep(0.002)

			
		while int(rob.x_pos.value) > end[0]:
			if rob.cliff_left.value or rob.cliff_right.value or rob.distance_front.value < 8 or rob.distance_IF_left.value < 9 :
				return False
				break
			rob.forward(0.001)
			time.sleep(0.0015)
			
	#move alonge the x axis (up)
	elif end[0] > start[0]:
		print("I am driving up")
		while int(rob.x_pos.value) < end[0]:
			if rob.cliff_left.value or rob.cliff_right.value or rob.distance_front.value < 8 or rob.distance_IF_left.value < 9 :
				return False
				break
			rob.forward(0.001)
			time.sleep(0.0015)
			

	#go right or positiv y
	#look in the right direction
	# drive until end is reached
	if end[1] < start[1]:
		print("I am driving right")
		print("and my yaw value is " +str(rob.yaw_angle.value) + "and it should be " + str(rob.circle_value*3/4))
		yaw_end = (rob.circle_value*3/4)
		yaw_to_far = rob.circle_value /2
		while rob.yaw_angle.value > yaw_end or rob.yaw_angle.value < yaw_to_far:
			rob.rightturn(0.001)
			time.sleep(0.002)
		
		while  int(rob.y_pos.value) > end[1]:
			if rob.cliff_left.value or rob.cliff_right.value or rob.distance_front.value < 9 or rob.distance_IF_left.value < 9 : 
				return False
				break
			rob.forward(0.001)
			time.sleep(0.0015)
			
	#go left or negativ y
	elif end[1] > start[1]:
		print("I am driving left")
		yaw_end = (rob.circle_value/4)
		yaw_to_far = rob.circle_value /2
		while rob.yaw_angle.value < yaw_end or rob.yaw_angle.value > yaw_to_far:
			print("and my yaw value is " +str(rob.yaw_angle.value) + "and it should be " + str(rob.circle_value/4))
			rob.leftturn(0.001)
			time.sleep(0.002)
			
		while  int(rob.y_pos.value)  < end[1] :
			if rob.cliff_left.value or rob.cliff_right.value or rob.distance_front.value < 9 or rob.distance_IF_left.value < 9 : 
				return False
				break
			rob.forward(0.001)
			time.sleep(0.0015)
			
	return True

def calculate_node_in_resepect_to_robot(rob,dest):
	yaw = rob.yaw_angle.value
	yaw = yaw *360 /rob.circle_value
	#put deg to rad
	yaw = (math.pi / 180) * yaw
	new_x_to_rob = math.cos(yaw) * dest[0] + math.sin(yaw) * dest[1] * (-1)
	new_y_to_rob = math.sin(yaw) * dest[0] + math.cos(yaw) * dest[1]
	
	return [int(new_x_to_rob), int(new_y_to_rob)] 

def reset_yaw(rob):
	#turn in the shorter dist. saves time
	if rob.yaw_angle.value > (rob.circle_value /2):
		while rob.yaw_angle.value > (rob.circle_value *0.025) :
			rob.leftturn(0.0001)
			time.sleep(0.0002)
	else:
		while rob.yaw_angle.value > (rob.circle_value *0.025) :
			rob.rightturn(0.0001)
			time.sleep(0.0002)
	
def drive_to(rob,Map, destination):
	x_pos = int(rob.x_pos.value)
	y_pos = int(rob.y_pos.value)
	#check if already there. If so, pass all. 
	if x_pos == destination[0] and y_pos == destination[1]:
		return True
		
	path = a_star.astar(Map, (int(x_pos),int(y_pos)), destination)
	print("Planned Path from: " + str((x_pos,y_pos)) + " to " + str(destination)+ "Path: "+ str(path))
	#check if there is a pos. path:
	if path[1]:
		# if there is, just drive along the nodes
		for nodes in path[0]:
			nextNode = calculate_node_in_resepect_to_robot(rob,nodes)
			print("next Node: " +str(nodes) +" Next Node converted: " + str(nextNode) + " position now: "+ str((x_pos,y_pos)))
			res = drive(rob, (x_pos,y_pos,), nodes)
			reset_yaw(rob)
			#update pos
			x_pos = int(rob.x_pos.value)
			y_pos = int(rob.y_pos.value)
			time.sleep(0.05)
			if not res:
				return False
	# if there is no path, return false
	else:
		return False

	return True

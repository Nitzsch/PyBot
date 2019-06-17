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
	#go down
	if end[0] < start[0]:
		while rob.x_pos.value > end[0]:
			rob.backward(0.001)
			time.sleep(0.0015)
			if rob.cliff_left.value or rob.cliff_right.value:
				return False
	#go up
	if end[0] > start[0]:
		while rob.x_pos.value < end[0]:
			rob.forward(0.001)
			time.sleep(0.0015)
			if rob.cliff_left.value or rob.cliff_right.value:
				return False
	#go left
	#look in the right direction
	# drive until end is reached
	if end[1] < start[1]:
		y_before = rob.y_pos.value
		while rob.yaw_angle.value > 165 or (rob.yaw_angle.value == 0):
			rob.rightturn(0.001)
			time.sleep(0.002)
		y_after = rob.y_pos.value	
		y_diff = y_after - y_before

		while  rob.y_pos.value - y_diff +1 > end[1]:
			rob.forward(0.001)
			time.sleep(0.0015)
			if rob.cliff_left.value or rob.cliff_right.value:
				return False
	#go right
	if end[1] > start[1]:
		while rob.yaw_angle.value < 165:
			rob.rightturn(0.001)
			time.sleep(0.0011)
		add_val = rob.y_pos.value -start[1]	
		while rob.y_pos.value - add_val > end[1]:
			rob.forward(0.001)
			time.sleep(0.0015)
			if rob.cliff_left.value or rob.cliff_right.value:
				return False
	return True

def calculate_node_in_resepect_to_robot(rob,dest):
	yaw = rob.yaw_angle.value
	#put deg to rad
	yaw = (math.pi / 180) * yaw
	new_x_to_rob = math.cos(yaw) * dest[0] + math.sin(yaw) * dest[1] * (-1)
	new_y_to_rob = math.sin(yaw) * dest[0] + math.cos(yaw) * dest[1]
	
	return [new_x_to_rob, new_y_to_rob] 
	
	
def drive_to(rob,Map, destination):
	x_pos = rob.x_pos.value
	y_pos = rob.y_pos.value

	path = a_star.astar(Map, (int(x_pos),int(y_pos)), destination)

	#check if there is a pos. path:
	if path[1]:
		# if there is, just drive along the nodes
		for nodes in path[0]:
			res = drive(rob, (x_pos,y_pos,), calculate_node_in_resepect_to_robot(rob,nodes))
			if not res:
				return False
			# update our pos
			x_pos = rob.x_pos.value
			y_pos = rob.y_pos.value

	return True

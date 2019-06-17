"""
Stuff thats done:

1. rob is at 0,0
2. rob checks surroundings and puts them in unvisited if ree
3. rob goes in while loop:
    a) as long as unvisited is not empty
    b) pop next node
    c) drive there
    d) check surroundings
    e) put them in unvisited, loop

"""
import drive_by_mouse as driver


def check_surroundings(rob,m):
    #first add left, then right, then front.
    # this order is maintained for mapping. the next node is always last added
    # so with this the rob will prefer order front > right >left
    if(rob.distance_left.value > m.resolution):
        m.addPos(int(rob.x_pos.value), int(rob.y_pos.value) -1, True)
    else:
        m.addPos(int(rob.x_pos.value), int(rob.y_pos.value) -1, False)

    if (rob.distance_right.value > m.resolution):
        m.addPos(int(rob.x_pos.value), int(rob.y_pos.value) +1, True)
    else:
        m.addPos(int(rob.x_pos.value), int(rob.y_pos.value) +1, False)

    if (rob.distance_front.value > m.resolution) and (rob.distance_IF_right.value > m.resolution) and (rob.distance_IF_left.value > m.resolution):
        m.addPos(int(rob.x_pos.value) + 1, int(rob.y_pos.value), True)
    else:
        m.addPos(int(rob.x_pos.value) +1 , int(rob.y_pos.value), False)


def start(rob, m):
    #init the mapping process bei checking the surroundings
    check_surroundings(rob,m)
    #then go into while loop while all is checked.
    while len(m.unvisitedNodes) > 0:
        next_to_check = m.unvisitedNodes.pop()
        # got to the node with driver
        drive = driver.drive_to(rob,m, next_to_check)
        # returns true if everything is ok
        # if not, the node is marked false or there is a cliff instead of a wall
        # so we have to remark the node
        # if everything is ok, we just check the surroundings of our new pos.
        if not drive:
            m.addPos(next_to_check[0], next_to_check[1], False)
        else:
            check_surroundings(rob,m)

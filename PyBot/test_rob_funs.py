import time
import robot
import mapping.map as Map
import mapping.a_star as a_star
import mapping.map_printer as map_print
import mapping.map_creator as creator
import mapping.drive_by_mouse as drive_by_mouse
if __name__ == '__main__':
    start_time = time.time()
    r = robot.Pybot()
    m = Map.Map(r)
    #time.sleep(0.5)
    m.addSquare(20)
    p = a_star.astar(m,(0, 0), (12,11))
    map_print.printer(m, p[0] ,[])
    
    #creator.check_surroundings(r,m)
    #go_to = m.unvisitedNodes.pop()
    #print(m.unvisitedNodes)

    #print(r.x_pos.value,r.y_pos.value)
    #drive_by_mouse.drive(r,(0,0), (1,0))
    #print(r.x_pos.value,r.y_pos.value)
    
    #print(r.x_pos.value,r.y_pos.value)
    #drive_by_mouse.drive(r,(0,0), (-1,0))
    #print(r.x_pos.value,r.y_pos.value)
    
    #print(r.x_pos.value,r.y_pos.value)
    #drive_by_mouse.drive(r,(0,0), (0,1))
    #print(r.x_pos.value,r.y_pos.value)
    #m.addEmptySquare(20)
    #time.sleep(0.5)
    #drive_by_mouse.drive(r,(0,0), (0,-1))
    #print(r.x_pos.value,r.y_pos.value)

    
    
    end_time = time.time()
    print(end_time - start_time)
    #print(go_to)
